<%inherit file="base.mako"/>
<%namespace name="lib" file="lib.mako"/>

<h2>All projects macros :</h2>

<!-- start force push dialog -->
${lib.publish_new_branch_dialog()}
<!-- end new branch to dialog -->

<div class="tab-pane" id="macros">
%for project in dict_project_to_macros :
  <h3><a href="${url(route_name='project_edit',id=project.id)}">Project : ${project.name}</a></h3>
  <ul id="macros_list">
    %for macro in dict_project_to_macros[project] :
     <li style="list-style:none;margin-bottom:0.4em;">
      <span class="macro_label" data-macro_id="${macro.id}">${macro.label}</span><br><span class="macro_content">${macro.get_description()}</span>
      <button class="btn btn-primary" onclick="run_this_macro(this, '${macro.label}','${url(route_name='macro_run', id=project.id, macro_id=macro.id)}');">run it</button>
     </li>
    %endfor
  </ul>
%endfor
</div>
