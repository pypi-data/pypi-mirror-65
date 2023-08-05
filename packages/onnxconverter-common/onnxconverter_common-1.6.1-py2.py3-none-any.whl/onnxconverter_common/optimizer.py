# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import six
import numpy as np
import onnx
from onnx import helper
from onnx import onnx_pb as onnx_proto


class LinkedNode(object):
    UNIQUE_NAME_INDEX = 0

    def __init__(self, node=None, in_n=None, out_n=None):
        self.origin = node  # type: onnx_proto.NodeProto
        if in_n is None and node is not None:
            in_n = node.input
        if out_n is None and node is not None:
            out_n = node.output
        self.input = {} if in_n is None else {i_: i_ for i_ in in_n}
        self.output = {} if out_n is None else {o_: o_ for o_ in out_n}
        self.precedence = []
        self.successor = []
        self.attributes = {}
        self.tensors = []
        LinkedNode.UNIQUE_NAME_INDEX += 1
        self.unique_name = "{}__{}".format(
            self.origin.name if self.origin and self.origin.name else 'unnamed',
            str(LinkedNode.UNIQUE_NAME_INDEX))

    def __repr__(self):
        return "name: {}, node: <{}>".format(self.unique_name, str(self.origin) if self.origin else 'None')

    @property
    def op_type(self):
        return None if self.origin is None else self.origin.op_type

    @property
    def is_identity(self):
        return False if self.origin is None else self.origin.op_type == 'Identity'

    @property
    def is_transpose(self):
        return False if self.origin is None else self.origin.op_type == 'Transpose'

    @property
    def in_single_path(self):
        """
        Test if a node is not linking to any fan in or out node.
        """
        return len(self.successor) == 1 and not self.successor[0].in_or_out and \
               len(self.precedence) == 1

    @property
    def element_wise(self):
        return False if self.origin is None else \
            self.origin.op_type in ['Relu', 'LeakyRelu', 'PRelu', 'Tanh'] + \
            ['Abs', 'Acos', 'Acosh', 'Log', 'Affine', 'Elu'] + \
            ['Sigmoid', 'ScaledTanh', 'HardSigmoid', 'Softsign', 'Softplus', 'Identity']

    @property
    def broadcast(self):
        return False if self.origin is None else \
            self.origin.op_type in ['Add', 'Div', 'Max']

    @property
    def in_single_path_and_inner(self):
        """
        Test if a node is not linking to any fan in or out node.
        """
        return len(self.successor) == 1 and self.successor[0] is not None and not self.successor[0].in_or_out and \
               len(self.precedence) == 1 and self.precedence[0] is not None and not self.precedence[0].in_or_out

    @property
    def in_simo_and_inner(self):
        """
        Test if a node is simo: single input and multiple output
        """
        return len(self.successor) > 1 and self.successor[0] is not None and not self.successor[0].in_or_out and \
               len(self.precedence) == 1 and self.precedence[0] is not None and not self.precedence[0].in_or_out

    @property
    def in_miso_and_inner(self):
        """
        Test if a node is miso: multiple input and single output
        """
        return len(self.successor) == 1 and self.successor[0] is not None and not self.successor[0].in_or_out and \
               len(self.precedence) > 1 and self.precedence[0] is not None and not self.precedence[0].in_or_out

    @property
    def in_mi_and_inner(self):
        """
        Test if a node is mi: multiple input
        """
        if len(self.precedence) < 1:
            return False
        for pre_ in self.precedence:
            if len(pre_.successor) > 1:
                return False
        return len(self.successor) >= 1 and \
               len(self.precedence) > 1 and self.precedence[0] is not None and not self.successor[0].in_or_out

    @property
    def is_eligible_concat_and_inner(self):
        """
        Test if a node is eligible_concat_and_inner: multiple input
        """
        if self.origin.op_type != 'Concat':
            return (False, None)
        perm = None
        for pre_ in self.precedence:
            if len(pre_.successor) > 1:
                return (False, None)
            if not hasattr(pre_.origin, 'op_type') or pre_.origin.op_type != 'Transpose':
                return (False, None)
            cur_perm = Solution.get_perm(pre_.origin)
            if perm and cur_perm != perm:
                return (False, None)
            perm = cur_perm
        for suc_ in self.successor:
            if suc_.in_or_out:
                return (False, None)
        axis = next(helper.get_attribute_value(attr) for attr in self.origin.attribute if attr.name == 'axis')
        if len(perm) <= axis:
            if perm == [] and axis == 0:
                return (True, -1)
            else:
                return (False, None)
        return (True, perm[axis])

    @property
    def is_transpose_switchable(self):
        return self.element_wise or self.broadcast

    @property
    def is_transpose_switchable_single_path(self):
        return self.in_single_path_and_inner and self.is_transpose_switchable

    @property
    def is_transpose_switchable_simo(self):
        return self.in_simo_and_inner and self.is_transpose_switchable

    @property
    def is_transpose_switchable_miso(self):
        return self.in_miso_and_inner and self.is_transpose_switchable

    @property
    def is_transpose_switchable_mi(self):
        return self.in_mi_and_inner and self.is_transpose_switchable

    @property
    def in_or_out(self):
        return self.origin is None

    @property
    def single_input(self):
        assert self.origin is not None and len(self.input) == 1
        return next(value for (key, value) in six.iteritems(self.input))

    @property
    def single_origin_input(self):
        assert self.origin is not None and len(self.input) == 1
        return self.origin.input[0]

    @property
    def single_output(self):
        assert self.origin is not None and len(self.output) == 1
        return next(value for (key, value) in six.iteritems(self.output))

    @property
    def single_origin_output(self):
        assert self.origin is not None and len(self.output) == 1
        return self.origin.output[0]

    def in_redirect(self, old_name, name):
        if old_name in self.input:
            self.input[old_name] = name
        else:
            key = next(k for k, v in six.iteritems(self.input) if v == old_name)
            self.input[key] = name

    def out_redirect(self, old_name, name):
        assert self.in_or_out
        if old_name in self.output:
            self.output[old_name] = name
        else:
            key = next(k for k, v in six.iteritems(self.output) if v == old_name)
            self.output[key] = name

    def reshape_input_for_broadcast(self, perm):
        assert len(self.origin.input) == 2
        self.tensors.append((np.reshape, self.origin.input[1]))

    def generate(self):
        updated = False
        if self.attributes or self.tensors:
            updated = True
        elif len([k for k, v in six.iteritems(self.input) if k != v]) > 0:
            updated = True
        elif len([k for k, v in six.iteritems(self.output) if k != v]) > 0:
            updated = True
        if not updated:
            return [self.origin]
        else:
            onode = onnx_proto.NodeProto()
            onode.name = self.origin.name
            onode.op_type = self.origin.op_type
            onode.input.extend([self.input.get(i_, i_) for i_ in self.origin.input])
            onode.output.extend([self.output.get(o_, o_) for o_ in self.origin.output])
            onode.doc_string = self.origin.doc_string
            onode.domain = self.origin.domain
            onode.attribute.extend(
                attr for attr in self.origin.attribute if attr.name not in self.attributes)
            onode.attribute.extend(
                helper.make_attribute(attr.name, self.attributes[attr.name]) for attr in self.attributes)

            return [onode] + self.tensors

    def add_precedence(self, pre, tname):
        self.precedence.append(pre)
        pre.successor.append(self)
        assert tname in self.input.values() and tname in pre.output.values()

    @staticmethod
    def build_from_onnx(onnx_nodes, nchw_inputs, inputs, outputs):
        view = []
        var_map = {}
        for o_ in onnx_nodes:
            ln = LinkedNode(o_)
            view.append(ln)
            for var_ in o_.output:
                assert var_map.get(var_) is None
                var_map[var_] = ln

        additional_nodes = []
        count_nchw = 0
        for n_ in view:
            for var_ in n_.origin.input:
                target = var_map.get(var_)
                if target is None:
                    assert var_ == '' or var_ in inputs
                    target = LinkedNode(out_n=[var_])  # create an empty node as input
                    new_output = var_ + '_nhwc'
                    if var_ in nchw_inputs:
                        nnode = LinkedNode(
                            helper.make_node(
                                'Transpose',
                                [var_],
                                [new_output],
                                name='Transpose_nchw_' + str(count_nchw),
                                perm=[0, 2, 3, 1]))
                        count_nchw = count_nchw + 1
                        var_map[new_output] = nnode
                        nnode.add_precedence(target, var_)
                        n_.in_redirect(var_, new_output)
                        target = nnode
                        var_ = new_output
                        additional_nodes.append(nnode)

                n_.add_precedence(target, var_)

        for n_ in view:  # add a dummy output node.
            for var_ in n_.origin.output:
                if var_ in outputs:
                    LinkedNode(in_n=[var_]).add_precedence(n_, var_)

        return view + additional_nodes

    @staticmethod
    def debug_print(node_list):
        for n_ in node_list:
            input_list = []
            output_list = []
            for pred in n_.precedence:
                if pred.origin is not None and pred.origin.name is not None:
                    input_list.append(pred.origin.name)
                else:
                    input_list.append("None")
            for succ in n_.successor:
                if succ.origin is not None and succ.origin.name is not None:
                    output_list.append(succ.origin.name)
                else:
                    output_list.append("None")
            input_list_str = ""
            if input_list is not None and input_list:
                input_list_str = ", ".join(input_list)
            output_list_str = ""
            if output_list is not None and output_list:
                output_list_str = ", ".join(output_list)
            print(
                "Node origin name: " + n_.origin.name + ", Input id: " + input_list_str + ", Output id: " + output_list_str)


class Solution(object):
    """
    Solution is the base class for solutions, and it has a basic function is to
     delete the node range of (begin, begin_n, end_p, end), where 'begin' and 'end' are excluded.
    """

    def __init__(self, begin, begin_n, end_p, end):
        self.begin = begin
        self.begin_n = begin_n
        self.end_p = end_p
        self.end = end

    @staticmethod
    def get_perm(onode):
        try:
            return next(
                helper.get_attribute_value(attr) for attr in onode.attribute if attr.name == 'perm')
        except StopIteration:
            return []

    @staticmethod
    def is_useless_transpose(perm):
        return perm == list(six.moves.range(len(perm)))

    @staticmethod
    def delete_node_nto1(node_list, begin, node, end):  # type: ([],LinkedNode, LinkedNode, LinkedNode)->[]
        """
        delete the node which has n-input and 1-output
        """
        if begin is None:
            assert node is not None
            begin = node.precedence
        elif not isinstance(begin, list):
            begin = [begin]

        if end.in_or_out:
            # if the end is output node, the output name will be kept to avoid the model output name updating.
            for nb_ in begin:
                nb_.out_redirect(node.single_input, node.single_output)
        else:
            for nb_ in begin:
                target_var_name = node.single_input
                assert target_var_name in nb_.output.values()  # since the output info never be updated, except the final.
                end.in_redirect(node.single_output, target_var_name)

        for nb_ in begin:
            nb_.successor = [end if v_ == node else v_ for v_ in nb_.successor]
        end.precedence = [v_ for v_ in end.precedence if v_ != node] + node.precedence

        node_list.remove(node)
        return node_list

    @staticmethod
    def delete_node_1ton(node_list, begin, node, end):  # type: ([],LinkedNode, LinkedNode, LinkedNode)->[]
        """
        delete the node which has 1-input and n-output
        """
        if end is None:
            assert end is not None
            end = node.successor
        elif not isinstance(end, list):
            end = [end]

        if any(e_.in_or_out for e_ in end):
            # if the end is output node, the output name will be kept to avoid the model output name updating.
            begin.out_redirect(node.single_input, node.single_output)
        else:
            for ne_ in end:
                target_var_name = node.single_input
                # since the output info never be updated, except the final.
                assert target_var_name in begin.output.values()
                ne_.in_redirect(node.single_output, target_var_name)

        begin.successor = [v_ for v_ in begin.successor if v_ != node] + node.successor
        for ne_ in end:
            ne_.precedence = [begin if v_ == node else v_ for v_ in ne_.precedence]

        node_list.remove(node)
        return node_list

    @staticmethod
    def add_siso_node(node_list, begin, end, begin_output_name, node):
        # type: ([], LinkedNode, LinkedNode, str, LinkedNode)->[]
        node.in_redirect(node.single_input, begin_output_name)
        end.in_redirect(begin_output_name, node.single_output)
        begin.successor[begin.successor.index(end)] = node
        end.precedence[end.precedence.index(begin)] = node
        node.precedence.append(begin)
        node.successor.append(end)
        node_list.append(node)

        return node_list

    def apply(self, node_list):
        node = self.begin_n  # type: LinkedNode
        while node != self.end:
            assert len(node.successor) == 1
            end = node.successor[0]
            if self.begin:
                node_list = self.delete_node_nto1(node_list, self.begin, node, end)
            else:
                node_list = self.delete_node_nto1(node_list, self.begin, node, end)
            node = self.end if self.end is None else end

        return node_list


# Match two perms where the merge is identity, this is order sensitive.
def match_perm(perm0, perm1):
    if len(perm0) != len(perm1):
        return False
    if perm0 == [] and perm1 == []:
        return True
    perm_f = [perm0[idx] for idx in perm1]
    return Solution.is_useless_transpose(perm_f)


class MergeSolution(Solution):
    def apply(self, node_list):
        perm0 = self.get_perm(self.begin_n.origin)
        perm1 = self.get_perm(self.end_p.origin)
        assert len(perm0) == len(perm1)
        perm_f = [perm0[idx] for idx in perm1]
        if self.is_useless_transpose(perm_f):
            node = self.begin  # type: LinkedNode
            while node != self.end and len(node.successor) >= 1:
                # if node.broadcast:
                #    node.reshape_input_for_broadcast(perm0)
                node = node.successor[0]

            node_list = self.delete_node_1ton(node_list, self.begin, self.begin_n, self.begin_n.successor[0])
            node_list = self.delete_node_1ton(node_list, self.end_p.precedence[0], self.end_p, self.end)
        else:
            node_list = self.delete_node_1ton(node_list, self.begin_n, self.end_p, self.end)
            self.begin_n.origin = helper.make_node('Transpose', self.begin_n.origin.input, self.begin_n.origin.output,
                                                   self.begin_n.origin.name, perm=perm_f)
        return node_list


class MoveForwardSolution(Solution):
    def apply(self, node_list):
        self.begin_n.successor[0].in_redirect(self.begin_n.single_output, self.begin.single_output)
        self.begin_n.in_redirect(self.begin.single_output, self.end_p.single_output)
        self.end.in_redirect(self.end_p.single_output, self.begin_n.single_output)

        self.begin_n.successor[0].precedence[0] = self.begin
        self.begin.successor[0] = self.begin_n.successor[0]
        self.begin_n.precedence[0] = self.end_p
        self.end_p.successor[0] = self.begin_n
        pre_len = len(self.end.precedence)
        for i_ in range(pre_len):
            if self.end.precedence[i_].origin and self.end.precedence[i_].origin.name == self.end_p.origin.name:
                self.end.precedence[i_] = self.begin_n
                break
        self.begin_n.successor[0] = self.end
        return node_list


class FanOutSolution(Solution):
    number = 0

    def apply(self, node_list):
        cur_perm = Solution.get_perm(self.begin_n.origin)
        # make a copy of self.end_p.successor
        successor_list = list(self.end_p.successor)

        for suc in successor_list:
            if cur_perm == []:
                nnode = LinkedNode(
                    helper.make_node(
                        'Transpose',
                        ['fan_out_adjustment_in' + str(FanOutSolution.number)],
                        ['fan_out_adjustment_out' + str(FanOutSolution.number)],
                        name='TransposeFanOut' + str(FanOutSolution.number)))
            else:
                nnode = LinkedNode(
                    helper.make_node(
                        'Transpose',
                        ['fan_out_adjustment_in' + str(FanOutSolution.number)],
                        ['fan_out_adjustment_out' + str(FanOutSolution.number)],
                        perm=cur_perm,
                        name='TransposeFanOut' + str(FanOutSolution.number)))
            FanOutSolution.number = FanOutSolution.number + 1
            node_list = Solution.add_siso_node(node_list, self.end_p, suc, list(self.end_p.output.values())[0], nnode)

        node_list = Solution.delete_node_1ton(node_list, self.begin, self.begin_n, self.end_p)
        return node_list


class TransposeFanOutSolution(Solution):
    def apply(self, node_list):
        successor_list = list(self.begin_n.successor)
        for suc_ in successor_list:
            node_list = Solution.delete_node_1ton(node_list, self.begin_n, suc_, suc_.successor[0])
        node_list = Solution.delete_node_1ton(node_list, self.begin, self.begin_n, self.begin_n.successor)
        return node_list


class FanInSolution(Solution):
    number = 0

    def __init__(self, begin, begin_n, end_p, end, perm):
        Solution.__init__(self, begin, begin_n, end_p, end)
        self.perm = perm

    def apply(self, node_list):
        # make a copy of self.begin.precedence
        precedence_list = list(self.begin.precedence)
        # make a copy of self.end_p.successor
        successor_list = list(self.begin.successor)

        for suc in successor_list:
            if self.perm == []:
                nnode = LinkedNode(
                    helper.make_node(
                        'Transpose',
                        ['fan_out_adjustment_in' + str(FanOutSolution.number)],
                        ['fan_out_adjustment_out' + str(FanOutSolution.number)],
                        name='TransposeFanIn_succ_' + str(FanOutSolution.number)))
            else:
                nnode = LinkedNode(
                    helper.make_node(
                        'Transpose',
                        ['fan_out_adjustment_in' + str(FanOutSolution.number)],
                        ['fan_out_adjustment_out' + str(FanOutSolution.number)],
                        perm=self.perm,
                        name='TransposeFanIn_succ_' + str(FanOutSolution.number)))
            FanOutSolution.number = FanOutSolution.number + 1
            node_list = Solution.add_siso_node(node_list, self.begin, suc, list(self.begin.output.values())[0], nnode)

        for branch in precedence_list:
            node_list = Solution.delete_node_1ton(node_list, branch.precedence[0], branch, self.begin)
        return node_list


class MergePadConvSolution(Solution):
    def __init__(self, begin, begin_n, end_p, end):
        Solution.__init__(self, begin, begin_n, end_p, end)

    def apply(self, node_list):
        pads = helper.get_attribute_value(self.begin_n.origin.attribute[1])
        half_len_pads = len(pads) // 2
        pads_new = pads[2:half_len_pads]
        pads_new.extend(pads[half_len_pads + 2:])
        attrs = {'pads': pads_new}
        pads_new = np.asarray(pads_new)
        auto_pad_value = helper.get_attribute_value(self.end_p.origin.attribute[0])
        if auto_pad_value == b'SAME_UPPER' or auto_pad_value == b'SAME_LOWER':
            return node_list

        for attr_idx in range(5):
            if attr_idx == 0:
                # for other cases, set auto_pad = 'NOTSET'
                attrs.update({'auto_pad': 'NOTSET'})
                continue
            cur_attr = self.end_p.origin.attribute[attr_idx]
            if cur_attr.name == "pads":
                conv_pads = np.asarray(helper.get_attribute_value(cur_attr))
                pads_new = list(pads_new + conv_pads)
                attrs.update({cur_attr.name: pads_new})
            else:
                attrs.update({cur_attr.name: helper.get_attribute_value(cur_attr)})

        self.end_p.origin = helper.make_node('Conv', self.end_p.origin.input, self.end_p.origin.output,
                                             self.end_p.origin.name + "_0", **attrs)

        node_list = Solution.delete_node_1ton(node_list, self.begin, self.begin_n, self.end_p)

        return node_list


class RedundantOptimizer(object):
    @staticmethod
    def find(node_list):
        solution = None
        for n_ in node_list:
            if n_.is_identity and n_.in_single_path:
                end = n_.successor[0]
                end_pre = n_
                while end is not None and end.is_identity and end.in_single_path:
                    end_pre = end
                    end = end.successor[0]
                solution = Solution(n_.precedence[0], n_, end_pre, end)
                return solution

        return solution


class TransposeOptimizer(object):
    @staticmethod
    def find(node_list):
        solution = None
        for n_ in node_list:
            if n_.is_transpose:
                perm = Solution.get_perm(n_.origin)
                if n_.in_single_path:  # n_.in_single_path_and_inner:
                    if Solution.is_useless_transpose(perm):
                        solution = Solution(n_.precedence[0], n_, n_, n_.successor[0])
                        return solution
                    else:
                        succ = n_.successor[0]  # type: LinkedNode
                        while succ.in_single_path:
                            if succ.is_transpose: break
                            if succ.element_wise or succ.broadcast:
                                succ = succ.successor[0]
                            else:
                                break
                        if succ.is_transpose:
                            solution = MergeSolution(n_.precedence[0], n_, succ, succ.successor[0])
                            return solution

                    last_switchable = n_
                    test_node = n_.successor[0]
                    switch_transpose = False
                    while test_node.is_transpose_switchable_single_path and not test_node.successor[0].in_or_out:
                        switch_transpose = True
                        last_switchable = test_node
                        test_node = test_node.successor[0]
                    if switch_transpose:
                        solution = MoveForwardSolution(n_.precedence[0], n_, last_switchable,
                                                       last_switchable.successor[0])
                        return solution

                    next_node = n_.successor[0]
                    if next_node.is_transpose_switchable_simo:
                        delta_node = -1
                        cur_perm = Solution.get_perm(n_.origin)
                        for branch in next_node.successor:
                            while branch.is_transpose_switchable_single_path:
                                branch = branch.successor[0]
                            if branch.is_transpose:
                                branch_perm = Solution.get_perm(branch.origin)
                                if len(cur_perm) == len(branch_perm):
                                    perm_f = [cur_perm[idx] for idx in branch_perm]

                                    if Solution.is_useless_transpose(perm_f):
                                        delta_node = delta_node - 1

                            else:
                                delta_node = delta_node + 1
                        if delta_node <= 0:
                            solution = FanOutSolution(n_.precedence[0], n_, next_node, None)
                            return solution
                else:  # simo Transpose op
                    simo_transpose_case = True
                    cur_perm = None
                    for succ_ in n_.successor:
                        if not succ_.is_transpose:
                            simo_transpose_case = False
                            break
                        if not cur_perm:
                            cur_perm = Solution.get_perm(succ_.origin)
                        elif cur_perm != Solution.get_perm(succ_.origin):
                            simo_transpose_case = False
                            break
                    if simo_transpose_case and match_perm(perm, cur_perm):
                        solution = TransposeFanOutSolution(n_.precedence[0], n_, None, None)
                        return solution
            elif n_.is_transpose_switchable_mi:
                branch_perm = []
                number_branch = 0
                good_branch = 0
                for branch in n_.precedence:
                    if branch.is_transpose and branch.in_single_path_and_inner:
                        if number_branch == 0:
                            branch_perm = Solution.get_perm(branch.origin)
                            good_branch = good_branch + 1
                        else:
                            cur_perm = Solution.get_perm(branch.origin)
                            if not branch_perm == cur_perm:
                                break
                            good_branch = good_branch + 1
                    else:
                        break
                    number_branch = number_branch + 1
                find_switch = good_branch == len(n_.precedence)

                if find_switch:
                    solution = FanInSolution(n_, n_.successor[0], None, None, branch_perm)
                    return solution
            eligible_concat = n_.is_eligible_concat_and_inner
            if eligible_concat[0]:
                perm = Solution.get_perm(n_.precedence[0].origin)
                solution = FanInSolution(n_, n_.successor[0], None, None, perm)
                onnx_node = helper.make_node('Concat', n_.origin.input, n_.origin.output,
                                             n_.origin.name, axis=eligible_concat[1])
                n_.origin = onnx_node
                return solution

        return solution


class MergePadConvOptimizer(object):
    @staticmethod
    def find(node_list):
        solution = None
        for n_ in node_list:
            if n_.origin.op_type == 'Pad' and n_.in_single_path_and_inner:
                next = n_.successor[0]
                if next.origin.op_type == 'Conv':
                    solution = MergePadConvSolution(n_.precedence[0], n_, next, next.successor[0])
                    return solution

        return solution


def _find_an_optimization(node_list):
    optimizers = (RedundantOptimizer, TransposeOptimizer, MergePadConvOptimizer)

    for optm in optimizers:
        solution = optm.find(node_list)
        if solution is not None:
            return solution

    return None


def _apply_optimization(solution, node_list):
    return solution.apply(node_list)


def _build_onnx_model(node_list):
    regenerated = []
    for n_ in node_list:
        nodes = n_.generate()
        regenerated.extend(nodes)
    return regenerated


def _visit(name_to_node_map, n_name, result):
    node = name_to_node_map[n_name]
    if node.status == 'perm':
        return
    if node.status == 'temp':
        raise Exception("This graph is not a DAG")
    node.status = 'temp'
    for m in node.successor:
        if m.origin is not None:
            _visit(name_to_node_map, m.name, result)
    node.status = 'perm'
    result.insert(0, node.idx)


def _topological_sort(node_list):
    name_to_node_map = dict()

    def _get_unmark_node(name_to_node_map):
        for k, v in six.iteritems(name_to_node_map):
            if v.status == 'unmark':
                return k
        return None

    result = []
    name_set = set()
    for idx_, n_ in enumerate(node_list):
        setattr(n_, 'idx', idx_)

    for n_ in node_list:
        name = n_.unique_name
        name_set.add(name)
        setattr(n_, 'name', name)
        setattr(n_, 'status', 'unmark')
        name_to_node_map.update({name: n_})

    n_name = _get_unmark_node(name_to_node_map)
    while n_name:
        _visit(name_to_node_map, n_name, result)
        n_name = _get_unmark_node(name_to_node_map)

    result_nodes = [node_list[result[idx]] for idx in range(len(node_list))]
    return result_nodes


def optimize_onnx(onnx_nodes, nchw_inputs=None, inputs=None, outputs=None):
    """
    Optimize onnx model by several approaches.
    :param onnx_nodes: the onnx node list in onnx model.
    :param opset opset: number of the model
    :param nchw_inputs: the name list of the inputs needed to be transposed as NCHW
    :param inputs: the model input
    :param outputs: the model output
    :return: the optimized onnx node list
    """
    node_list = LinkedNode.build_from_onnx(onnx_nodes,
                                           nchw_inputs if nchw_inputs else [],
                                           [] if inputs is None else [i_.name for i_ in inputs],
                                           [] if outputs is None else [o_.name for o_ in outputs])
    solution = _find_an_optimization(node_list)
    while solution:
        node_list = _apply_optimization(solution, node_list)
        solution = _find_an_optimization(node_list)

    node_list = _topological_sort(node_list)
    return _build_onnx_model(node_list)


def optimize_onnx_model(origin_model, nchw_inputs=None):
    """
    the origin model will be updated after the optimization.
    :param origin_model:
    :param nchw_inputs:
    :return:
    """
    graph = origin_model.graph
    nodelist = list(graph.node)

    input_with_initializer = [in_ for in_ in graph.input]
    input_with_initializer += [in_ for in_ in graph.initializer]
    all_nodes = optimize_onnx(nodelist,
                              nchw_inputs=nchw_inputs,
                              inputs=input_with_initializer,
                              outputs=graph.output)

    del graph.node[:]
    nodes = [n_ for n_ in all_nodes if not isinstance(n_, tuple)]
    graph.node.extend(nodes)

    alter_tensors = {n_[1]: n_[0] for n_ in all_nodes if isinstance(n_, tuple)}

    def update_tensor(x):
        helper.make_tensor(x.name, x.data_type, (x.dims[0], 1, 1),
                           onnx.numpy_helper.to_array(x).flatten())

    new_initializer = [init_ if init_.name not in alter_tensors else update_tensor(init_)
                       for init_ in graph.initializer]
    del graph.initializer[:]
    graph.initializer.extend(new_initializer)

    def update_value_info(x):
        helper.make_tensor_value_info(x.name, x.type.tensor_type.elem_type,
                                      (x.type.tensor_type.shape.dim[0].dim_value, 1, 1))

    new_input = [in_ if in_.name not in alter_tensors else update_value_info(in_)
                 for in_ in graph.input]
    del graph.input[:]
    graph.input.extend(new_input)
    return origin_model
