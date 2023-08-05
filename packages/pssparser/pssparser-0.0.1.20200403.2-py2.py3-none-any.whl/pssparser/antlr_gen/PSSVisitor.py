# Generated from PSS.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .PSSParser import PSSParser
else:
    from PSSParser import PSSParser

# This class defines a complete generic visitor for a parse tree produced by PSSParser.

class PSSVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PSSParser#compilation_unit.
    def visitCompilation_unit(self, ctx:PSSParser.Compilation_unitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#portable_stimulus_description.
    def visitPortable_stimulus_description(self, ctx:PSSParser.Portable_stimulus_descriptionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_declaration.
    def visitPackage_declaration(self, ctx:PSSParser.Package_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_body_item.
    def visitPackage_body_item(self, ctx:PSSParser.Package_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_stmt.
    def visitImport_stmt(self, ctx:PSSParser.Import_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_import_pattern.
    def visitPackage_import_pattern(self, ctx:PSSParser.Package_import_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#extend_stmt.
    def visitExtend_stmt(self, ctx:PSSParser.Extend_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#const_field_declaration.
    def visitConst_field_declaration(self, ctx:PSSParser.Const_field_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#const_data_declaration.
    def visitConst_data_declaration(self, ctx:PSSParser.Const_data_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#const_data_instantiation.
    def visitConst_data_instantiation(self, ctx:PSSParser.Const_data_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#static_const_field_declaration.
    def visitStatic_const_field_declaration(self, ctx:PSSParser.Static_const_field_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_declaration.
    def visitAction_declaration(self, ctx:PSSParser.Action_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#abstract_action_declaration.
    def visitAbstract_action_declaration(self, ctx:PSSParser.Abstract_action_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_super_spec.
    def visitAction_super_spec(self, ctx:PSSParser.Action_super_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_body_item.
    def visitAction_body_item(self, ctx:PSSParser.Action_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_declaration.
    def visitActivity_declaration(self, ctx:PSSParser.Activity_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_field_declaration.
    def visitAction_field_declaration(self, ctx:PSSParser.Action_field_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#object_ref_declaration.
    def visitObject_ref_declaration(self, ctx:PSSParser.Object_ref_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#flow_ref_declaration.
    def visitFlow_ref_declaration(self, ctx:PSSParser.Flow_ref_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#resource_ref_declaration.
    def visitResource_ref_declaration(self, ctx:PSSParser.Resource_ref_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#object_ref_field.
    def visitObject_ref_field(self, ctx:PSSParser.Object_ref_fieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#flow_object_type.
    def visitFlow_object_type(self, ctx:PSSParser.Flow_object_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#resource_object_type.
    def visitResource_object_type(self, ctx:PSSParser.Resource_object_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#attr_field.
    def visitAttr_field(self, ctx:PSSParser.Attr_fieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#access_modifier.
    def visitAccess_modifier(self, ctx:PSSParser.Access_modifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#attr_group.
    def visitAttr_group(self, ctx:PSSParser.Attr_groupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_handle_declaration.
    def visitAction_handle_declaration(self, ctx:PSSParser.Action_handle_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_instantiation.
    def visitAction_instantiation(self, ctx:PSSParser.Action_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_data_field.
    def visitActivity_data_field(self, ctx:PSSParser.Activity_data_fieldContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_scheduling_constraint.
    def visitAction_scheduling_constraint(self, ctx:PSSParser.Action_scheduling_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exec_block_stmt.
    def visitExec_block_stmt(self, ctx:PSSParser.Exec_block_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exec_block.
    def visitExec_block(self, ctx:PSSParser.Exec_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exec_kind_identifier.
    def visitExec_kind_identifier(self, ctx:PSSParser.Exec_kind_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exec_stmt.
    def visitExec_stmt(self, ctx:PSSParser.Exec_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exec_super_stmt.
    def visitExec_super_stmt(self, ctx:PSSParser.Exec_super_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#assign_op.
    def visitAssign_op(self, ctx:PSSParser.Assign_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#target_code_exec_block.
    def visitTarget_code_exec_block(self, ctx:PSSParser.Target_code_exec_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#target_file_exec_block.
    def visitTarget_file_exec_block(self, ctx:PSSParser.Target_file_exec_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_declaration.
    def visitStruct_declaration(self, ctx:PSSParser.Struct_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_kind.
    def visitStruct_kind(self, ctx:PSSParser.Struct_kindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#object_kind.
    def visitObject_kind(self, ctx:PSSParser.Object_kindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_super_spec.
    def visitStruct_super_spec(self, ctx:PSSParser.Struct_super_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_body_item.
    def visitStruct_body_item(self, ctx:PSSParser.Struct_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#function_decl.
    def visitFunction_decl(self, ctx:PSSParser.Function_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_prototype.
    def visitMethod_prototype(self, ctx:PSSParser.Method_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_return_type.
    def visitMethod_return_type(self, ctx:PSSParser.Method_return_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_parameter_list_prototype.
    def visitMethod_parameter_list_prototype(self, ctx:PSSParser.Method_parameter_list_prototypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_parameter.
    def visitMethod_parameter(self, ctx:PSSParser.Method_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_parameter_dir.
    def visitMethod_parameter_dir(self, ctx:PSSParser.Method_parameter_dirContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#function_qualifiers.
    def visitFunction_qualifiers(self, ctx:PSSParser.Function_qualifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_function_qualifiers.
    def visitImport_function_qualifiers(self, ctx:PSSParser.Import_function_qualifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_qualifiers.
    def visitMethod_qualifiers(self, ctx:PSSParser.Method_qualifiersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#target_template_function.
    def visitTarget_template_function(self, ctx:PSSParser.Target_template_functionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_parameter_list.
    def visitMethod_parameter_list(self, ctx:PSSParser.Method_parameter_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#pss_function_defn.
    def visitPss_function_defn(self, ctx:PSSParser.Pss_function_defnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_stmt.
    def visitProcedural_stmt(self, ctx:PSSParser.Procedural_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_block_stmt.
    def visitProcedural_block_stmt(self, ctx:PSSParser.Procedural_block_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_var_decl_stmt.
    def visitProcedural_var_decl_stmt(self, ctx:PSSParser.Procedural_var_decl_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_expr_stmt.
    def visitProcedural_expr_stmt(self, ctx:PSSParser.Procedural_expr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_return_stmt.
    def visitProcedural_return_stmt(self, ctx:PSSParser.Procedural_return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_if_else_stmt.
    def visitProcedural_if_else_stmt(self, ctx:PSSParser.Procedural_if_else_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_match_stmt.
    def visitProcedural_match_stmt(self, ctx:PSSParser.Procedural_match_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_match_choice.
    def visitProcedural_match_choice(self, ctx:PSSParser.Procedural_match_choiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_repeat_stmt.
    def visitProcedural_repeat_stmt(self, ctx:PSSParser.Procedural_repeat_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_foreach_stmt.
    def visitProcedural_foreach_stmt(self, ctx:PSSParser.Procedural_foreach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_break_stmt.
    def visitProcedural_break_stmt(self, ctx:PSSParser.Procedural_break_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#procedural_continue_stmt.
    def visitProcedural_continue_stmt(self, ctx:PSSParser.Procedural_continue_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_declaration.
    def visitComponent_declaration(self, ctx:PSSParser.Component_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_super_spec.
    def visitComponent_super_spec(self, ctx:PSSParser.Component_super_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_body_item.
    def visitComponent_body_item(self, ctx:PSSParser.Component_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_field_declaration.
    def visitComponent_field_declaration(self, ctx:PSSParser.Component_field_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_data_declaration.
    def visitComponent_data_declaration(self, ctx:PSSParser.Component_data_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_pool_declaration.
    def visitComponent_pool_declaration(self, ctx:PSSParser.Component_pool_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#object_bind_stmt.
    def visitObject_bind_stmt(self, ctx:PSSParser.Object_bind_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#object_bind_item_or_list.
    def visitObject_bind_item_or_list(self, ctx:PSSParser.Object_bind_item_or_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_path.
    def visitComponent_path(self, ctx:PSSParser.Component_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_path_elem.
    def visitComponent_path_elem(self, ctx:PSSParser.Component_path_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_stmt.
    def visitActivity_stmt(self, ctx:PSSParser.Activity_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#labeled_activity_stmt.
    def visitLabeled_activity_stmt(self, ctx:PSSParser.Labeled_activity_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_if_else_stmt.
    def visitActivity_if_else_stmt(self, ctx:PSSParser.Activity_if_else_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_repeat_stmt.
    def visitActivity_repeat_stmt(self, ctx:PSSParser.Activity_repeat_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_replicate_stmt.
    def visitActivity_replicate_stmt(self, ctx:PSSParser.Activity_replicate_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_sequence_block_stmt.
    def visitActivity_sequence_block_stmt(self, ctx:PSSParser.Activity_sequence_block_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_constraint_stmt.
    def visitActivity_constraint_stmt(self, ctx:PSSParser.Activity_constraint_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_foreach_stmt.
    def visitActivity_foreach_stmt(self, ctx:PSSParser.Activity_foreach_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_action_traversal_stmt.
    def visitActivity_action_traversal_stmt(self, ctx:PSSParser.Activity_action_traversal_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_select_stmt.
    def visitActivity_select_stmt(self, ctx:PSSParser.Activity_select_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#select_branch.
    def visitSelect_branch(self, ctx:PSSParser.Select_branchContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_match_stmt.
    def visitActivity_match_stmt(self, ctx:PSSParser.Activity_match_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#match_choice.
    def visitMatch_choice(self, ctx:PSSParser.Match_choiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_parallel_stmt.
    def visitActivity_parallel_stmt(self, ctx:PSSParser.Activity_parallel_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_schedule_stmt.
    def visitActivity_schedule_stmt(self, ctx:PSSParser.Activity_schedule_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_join_spec.
    def visitActivity_join_spec(self, ctx:PSSParser.Activity_join_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_join_branch_spec.
    def visitActivity_join_branch_spec(self, ctx:PSSParser.Activity_join_branch_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_join_select_spec.
    def visitActivity_join_select_spec(self, ctx:PSSParser.Activity_join_select_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_join_none_spec.
    def visitActivity_join_none_spec(self, ctx:PSSParser.Activity_join_none_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_join_first_spec.
    def visitActivity_join_first_spec(self, ctx:PSSParser.Activity_join_first_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_bind_stmt.
    def visitActivity_bind_stmt(self, ctx:PSSParser.Activity_bind_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_bind_item_or_list.
    def visitActivity_bind_item_or_list(self, ctx:PSSParser.Activity_bind_item_or_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#symbol_declaration.
    def visitSymbol_declaration(self, ctx:PSSParser.Symbol_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#symbol_paramlist.
    def visitSymbol_paramlist(self, ctx:PSSParser.Symbol_paramlistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#symbol_param.
    def visitSymbol_param(self, ctx:PSSParser.Symbol_paramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#activity_super_stmt.
    def visitActivity_super_stmt(self, ctx:PSSParser.Activity_super_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#overrides_declaration.
    def visitOverrides_declaration(self, ctx:PSSParser.Overrides_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#override_stmt.
    def visitOverride_stmt(self, ctx:PSSParser.Override_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_override.
    def visitType_override(self, ctx:PSSParser.Type_overrideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#instance_override.
    def visitInstance_override(self, ctx:PSSParser.Instance_overrideContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#data_declaration.
    def visitData_declaration(self, ctx:PSSParser.Data_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#data_instantiation.
    def visitData_instantiation(self, ctx:PSSParser.Data_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_portmap_list.
    def visitCovergroup_portmap_list(self, ctx:PSSParser.Covergroup_portmap_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_portmap.
    def visitCovergroup_portmap(self, ctx:PSSParser.Covergroup_portmapContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#array_dim.
    def visitArray_dim(self, ctx:PSSParser.Array_dimContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#data_type.
    def visitData_type(self, ctx:PSSParser.Data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#container_type.
    def visitContainer_type(self, ctx:PSSParser.Container_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#array_size_expression.
    def visitArray_size_expression(self, ctx:PSSParser.Array_size_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#container_elem_type.
    def visitContainer_elem_type(self, ctx:PSSParser.Container_elem_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#container_key_type.
    def visitContainer_key_type(self, ctx:PSSParser.Container_key_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#scalar_data_type.
    def visitScalar_data_type(self, ctx:PSSParser.Scalar_data_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#chandle_type.
    def visitChandle_type(self, ctx:PSSParser.Chandle_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#integer_type.
    def visitInteger_type(self, ctx:PSSParser.Integer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#integer_atom_type.
    def visitInteger_atom_type(self, ctx:PSSParser.Integer_atom_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#domain_open_range_list.
    def visitDomain_open_range_list(self, ctx:PSSParser.Domain_open_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#domain_open_range_value.
    def visitDomain_open_range_value(self, ctx:PSSParser.Domain_open_range_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#string_type.
    def visitString_type(self, ctx:PSSParser.String_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#bool_type.
    def visitBool_type(self, ctx:PSSParser.Bool_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#user_defined_datatype.
    def visitUser_defined_datatype(self, ctx:PSSParser.User_defined_datatypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#enum_declaration.
    def visitEnum_declaration(self, ctx:PSSParser.Enum_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#enum_item.
    def visitEnum_item(self, ctx:PSSParser.Enum_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#enum_type.
    def visitEnum_type(self, ctx:PSSParser.Enum_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#enum_type_identifier.
    def visitEnum_type_identifier(self, ctx:PSSParser.Enum_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#typedef_declaration.
    def visitTypedef_declaration(self, ctx:PSSParser.Typedef_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#template_param_decl_list.
    def visitTemplate_param_decl_list(self, ctx:PSSParser.Template_param_decl_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#template_param_decl.
    def visitTemplate_param_decl(self, ctx:PSSParser.Template_param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_param_decl.
    def visitType_param_decl(self, ctx:PSSParser.Type_param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#generic_type_param_decl.
    def visitGeneric_type_param_decl(self, ctx:PSSParser.Generic_type_param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#category_type_param_decl.
    def visitCategory_type_param_decl(self, ctx:PSSParser.Category_type_param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_restriction.
    def visitType_restriction(self, ctx:PSSParser.Type_restrictionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_category.
    def visitType_category(self, ctx:PSSParser.Type_categoryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#value_param_decl.
    def visitValue_param_decl(self, ctx:PSSParser.Value_param_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#template_param_value_list.
    def visitTemplate_param_value_list(self, ctx:PSSParser.Template_param_value_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#template_param_value.
    def visitTemplate_param_value(self, ctx:PSSParser.Template_param_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constraint_declaration.
    def visitConstraint_declaration(self, ctx:PSSParser.Constraint_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constraint_body_item.
    def visitConstraint_body_item(self, ctx:PSSParser.Constraint_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#default_constraint_item.
    def visitDefault_constraint_item(self, ctx:PSSParser.Default_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#default_constraint.
    def visitDefault_constraint(self, ctx:PSSParser.Default_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#default_disable_constraint.
    def visitDefault_disable_constraint(self, ctx:PSSParser.Default_disable_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#forall_constraint_item.
    def visitForall_constraint_item(self, ctx:PSSParser.Forall_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#expression_constraint_item.
    def visitExpression_constraint_item(self, ctx:PSSParser.Expression_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#implicand_constraint_item.
    def visitImplicand_constraint_item(self, ctx:PSSParser.Implicand_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constraint_set.
    def visitConstraint_set(self, ctx:PSSParser.Constraint_setContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constraint_block.
    def visitConstraint_block(self, ctx:PSSParser.Constraint_blockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#foreach_constraint_item.
    def visitForeach_constraint_item(self, ctx:PSSParser.Foreach_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#if_constraint_item.
    def visitIf_constraint_item(self, ctx:PSSParser.If_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#unique_constraint_item.
    def visitUnique_constraint_item(self, ctx:PSSParser.Unique_constraint_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#single_stmt_constraint.
    def visitSingle_stmt_constraint(self, ctx:PSSParser.Single_stmt_constraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_declaration.
    def visitCovergroup_declaration(self, ctx:PSSParser.Covergroup_declarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_port.
    def visitCovergroup_port(self, ctx:PSSParser.Covergroup_portContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_body_item.
    def visitCovergroup_body_item(self, ctx:PSSParser.Covergroup_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_option.
    def visitCovergroup_option(self, ctx:PSSParser.Covergroup_optionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_instantiation.
    def visitCovergroup_instantiation(self, ctx:PSSParser.Covergroup_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#inline_covergroup.
    def visitInline_covergroup(self, ctx:PSSParser.Inline_covergroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_type_instantiation.
    def visitCovergroup_type_instantiation(self, ctx:PSSParser.Covergroup_type_instantiationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_coverpoint.
    def visitCovergroup_coverpoint(self, ctx:PSSParser.Covergroup_coverpointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#bins_or_empty.
    def visitBins_or_empty(self, ctx:PSSParser.Bins_or_emptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_coverpoint_body_item.
    def visitCovergroup_coverpoint_body_item(self, ctx:PSSParser.Covergroup_coverpoint_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_coverpoint_binspec.
    def visitCovergroup_coverpoint_binspec(self, ctx:PSSParser.Covergroup_coverpoint_binspecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#coverpoint_bins.
    def visitCoverpoint_bins(self, ctx:PSSParser.Coverpoint_binsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_range_list.
    def visitCovergroup_range_list(self, ctx:PSSParser.Covergroup_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_value_range.
    def visitCovergroup_value_range(self, ctx:PSSParser.Covergroup_value_rangeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#bins_keyword.
    def visitBins_keyword(self, ctx:PSSParser.Bins_keywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_cross.
    def visitCovergroup_cross(self, ctx:PSSParser.Covergroup_crossContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#cross_item_or_null.
    def visitCross_item_or_null(self, ctx:PSSParser.Cross_item_or_nullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_cross_body_item.
    def visitCovergroup_cross_body_item(self, ctx:PSSParser.Covergroup_cross_body_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_cross_binspec.
    def visitCovergroup_cross_binspec(self, ctx:PSSParser.Covergroup_cross_binspecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_expression.
    def visitCovergroup_expression(self, ctx:PSSParser.Covergroup_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_body_compile_if.
    def visitPackage_body_compile_if(self, ctx:PSSParser.Package_body_compile_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_body_compile_if_item.
    def visitPackage_body_compile_if_item(self, ctx:PSSParser.Package_body_compile_if_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_body_compile_if.
    def visitAction_body_compile_if(self, ctx:PSSParser.Action_body_compile_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_body_compile_if_item.
    def visitAction_body_compile_if_item(self, ctx:PSSParser.Action_body_compile_if_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_body_compile_if.
    def visitComponent_body_compile_if(self, ctx:PSSParser.Component_body_compile_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_body_compile_if_item.
    def visitComponent_body_compile_if_item(self, ctx:PSSParser.Component_body_compile_if_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_body_compile_if.
    def visitStruct_body_compile_if(self, ctx:PSSParser.Struct_body_compile_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_body_compile_if_item.
    def visitStruct_body_compile_if_item(self, ctx:PSSParser.Struct_body_compile_if_itemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#compile_has_expr.
    def visitCompile_has_expr(self, ctx:PSSParser.Compile_has_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#compile_assert_stmt.
    def visitCompile_assert_stmt(self, ctx:PSSParser.Compile_assert_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constant_expression.
    def visitConstant_expression(self, ctx:PSSParser.Constant_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#expression.
    def visitExpression(self, ctx:PSSParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#conditional_expr.
    def visitConditional_expr(self, ctx:PSSParser.Conditional_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#logical_or_op.
    def visitLogical_or_op(self, ctx:PSSParser.Logical_or_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#logical_and_op.
    def visitLogical_and_op(self, ctx:PSSParser.Logical_and_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#binary_or_op.
    def visitBinary_or_op(self, ctx:PSSParser.Binary_or_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#binary_xor_op.
    def visitBinary_xor_op(self, ctx:PSSParser.Binary_xor_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#binary_and_op.
    def visitBinary_and_op(self, ctx:PSSParser.Binary_and_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#inside_expr_term.
    def visitInside_expr_term(self, ctx:PSSParser.Inside_expr_termContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#open_range_list.
    def visitOpen_range_list(self, ctx:PSSParser.Open_range_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#open_range_value.
    def visitOpen_range_value(self, ctx:PSSParser.Open_range_valueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#logical_inequality_op.
    def visitLogical_inequality_op(self, ctx:PSSParser.Logical_inequality_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#unary_op.
    def visitUnary_op(self, ctx:PSSParser.Unary_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#exp_op.
    def visitExp_op(self, ctx:PSSParser.Exp_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#primary.
    def visitPrimary(self, ctx:PSSParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#paren_expr.
    def visitParen_expr(self, ctx:PSSParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#cast_expression.
    def visitCast_expression(self, ctx:PSSParser.Cast_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#casting_type.
    def visitCasting_type(self, ctx:PSSParser.Casting_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#variable_ref_path.
    def visitVariable_ref_path(self, ctx:PSSParser.Variable_ref_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_function_symbol_call.
    def visitMethod_function_symbol_call(self, ctx:PSSParser.Method_function_symbol_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_call.
    def visitMethod_call(self, ctx:PSSParser.Method_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#function_symbol_call.
    def visitFunction_symbol_call(self, ctx:PSSParser.Function_symbol_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#function_symbol_id.
    def visitFunction_symbol_id(self, ctx:PSSParser.Function_symbol_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#function_id.
    def visitFunction_id(self, ctx:PSSParser.Function_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#static_ref_path.
    def visitStatic_ref_path(self, ctx:PSSParser.Static_ref_pathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#static_ref_path_elem.
    def visitStatic_ref_path_elem(self, ctx:PSSParser.Static_ref_path_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#mul_div_mod_op.
    def visitMul_div_mod_op(self, ctx:PSSParser.Mul_div_mod_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#add_sub_op.
    def visitAdd_sub_op(self, ctx:PSSParser.Add_sub_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#shift_op.
    def visitShift_op(self, ctx:PSSParser.Shift_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#eq_neq_op.
    def visitEq_neq_op(self, ctx:PSSParser.Eq_neq_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#constant.
    def visitConstant(self, ctx:PSSParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#identifier.
    def visitIdentifier(self, ctx:PSSParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#hierarchical_id_list.
    def visitHierarchical_id_list(self, ctx:PSSParser.Hierarchical_id_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#hierarchical_id.
    def visitHierarchical_id(self, ctx:PSSParser.Hierarchical_idContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#hierarchical_id_elem.
    def visitHierarchical_id_elem(self, ctx:PSSParser.Hierarchical_id_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_type_identifier.
    def visitAction_type_identifier(self, ctx:PSSParser.Action_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_identifier.
    def visitType_identifier(self, ctx:PSSParser.Type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#type_identifier_elem.
    def visitType_identifier_elem(self, ctx:PSSParser.Type_identifier_elemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#package_identifier.
    def visitPackage_identifier(self, ctx:PSSParser.Package_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covercross_identifier.
    def visitCovercross_identifier(self, ctx:PSSParser.Covercross_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_identifier.
    def visitCovergroup_identifier(self, ctx:PSSParser.Covergroup_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#coverpoint_target_identifier.
    def visitCoverpoint_target_identifier(self, ctx:PSSParser.Coverpoint_target_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#action_identifier.
    def visitAction_identifier(self, ctx:PSSParser.Action_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#struct_identifier.
    def visitStruct_identifier(self, ctx:PSSParser.Struct_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_identifier.
    def visitComponent_identifier(self, ctx:PSSParser.Component_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#component_action_identifier.
    def visitComponent_action_identifier(self, ctx:PSSParser.Component_action_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#coverpoint_identifier.
    def visitCoverpoint_identifier(self, ctx:PSSParser.Coverpoint_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#enum_identifier.
    def visitEnum_identifier(self, ctx:PSSParser.Enum_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_class_identifier.
    def visitImport_class_identifier(self, ctx:PSSParser.Import_class_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#label_identifier.
    def visitLabel_identifier(self, ctx:PSSParser.Label_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#language_identifier.
    def visitLanguage_identifier(self, ctx:PSSParser.Language_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#method_identifier.
    def visitMethod_identifier(self, ctx:PSSParser.Method_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#symbol_identifier.
    def visitSymbol_identifier(self, ctx:PSSParser.Symbol_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#variable_identifier.
    def visitVariable_identifier(self, ctx:PSSParser.Variable_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#iterator_identifier.
    def visitIterator_identifier(self, ctx:PSSParser.Iterator_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#index_identifier.
    def visitIndex_identifier(self, ctx:PSSParser.Index_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#buffer_type_identifier.
    def visitBuffer_type_identifier(self, ctx:PSSParser.Buffer_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#covergroup_type_identifier.
    def visitCovergroup_type_identifier(self, ctx:PSSParser.Covergroup_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#resource_type_identifier.
    def visitResource_type_identifier(self, ctx:PSSParser.Resource_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#state_type_identifier.
    def visitState_type_identifier(self, ctx:PSSParser.State_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#stream_type_identifier.
    def visitStream_type_identifier(self, ctx:PSSParser.Stream_type_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#filename_string.
    def visitFilename_string(self, ctx:PSSParser.Filename_stringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#bool_literal.
    def visitBool_literal(self, ctx:PSSParser.Bool_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#number.
    def visitNumber(self, ctx:PSSParser.NumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#based_hex_number.
    def visitBased_hex_number(self, ctx:PSSParser.Based_hex_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#based_dec_number.
    def visitBased_dec_number(self, ctx:PSSParser.Based_dec_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#dec_number.
    def visitDec_number(self, ctx:PSSParser.Dec_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#based_bin_number.
    def visitBased_bin_number(self, ctx:PSSParser.Based_bin_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#based_oct_number.
    def visitBased_oct_number(self, ctx:PSSParser.Based_oct_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#oct_number.
    def visitOct_number(self, ctx:PSSParser.Oct_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#hex_number.
    def visitHex_number(self, ctx:PSSParser.Hex_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#string.
    def visitString(self, ctx:PSSParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_class_decl.
    def visitImport_class_decl(self, ctx:PSSParser.Import_class_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_class_extends.
    def visitImport_class_extends(self, ctx:PSSParser.Import_class_extendsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#import_class_method_decl.
    def visitImport_class_method_decl(self, ctx:PSSParser.Import_class_method_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PSSParser#export_action.
    def visitExport_action(self, ctx:PSSParser.Export_actionContext):
        return self.visitChildren(ctx)



del PSSParser