<%!
  import json
%>
<%inherit file="base.mako"/>
<%namespace name="lib" file="lib.mako"/>

<!-- start force push dialog -->
${lib.publish_new_branch_dialog()}
<!-- end new branch to dialog -->

<h1>
  <form name="rename_group" action="${url(route_name='group_rename', id=group.id)}">
    <input name="name" value="${group.name}">
    <button class="btn">rename</button>
  </form>
</h1>
## 
## present all projects linked to this group
## 

<br>
<div class="list-group row">
  <div class="list-group col-md-4">
    <a href="#" class="list-group-item active"> ${group.name}<span class="badge">${len(group.projects)}</span></a>
    % for __project in sorted((p for p in group.projects if p.id in set_projects_list_id), key=lambda x: x.name):
      <a class="list-group-item" href="${url(route_name='project_edit',id=__project.id)}">-> <i>${__project.name}</i> project
         <button type="button" class="close" onclick="remove_that_project_from_that_group(this, '${url('group_detach',id=__project.id, group_id=group.id)}', '${url('projects_list_global')}'); return false;">×</button>
      </a>
    % endfor
  </div>
  <div class="list-group col-md-1">
    <button class="btn btn-danger" onclick="go_to('${url(route_name='project_group_delete', id=group.id)}')">delete this group</button>
  </div>
</div>


% if len(dict_project_to_macros)>0 :
  <div class="list-group row">
  <h1> macros into ${group.name} </h1>
  
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
% else :
  <div class="list-group row">
  <h1>macros into ${group.name}</h1>
  <i>no macro recorded</i>
  </div>
% endif


% if len(dict_project_to_tasks)>0 :
  <div class="list-group row">
    <h1> tasks into ${group.name} </h1>
    %for project in dict_project_to_tasks :
      <h3><a href="${url(route_name='project_edit',id=project.id)}">Project : ${project.name}</a></h3>
      <ul id="tasks_list">
        %for task in dict_project_to_tasks[project] :
         <li>
              <input type="text" name="task_content" value="${task.content}">
              <button data-id="${task.id}" data-url="${url(route_name='project_run_task', id=task.id)}" onclick="run_this_task(this)" type="button" class="btn">run it ..</button>
         </li>
        %endfor
      </ul>
    %endfor
  </div>
% else :
  <div class="list-group row">
    <h1> tasks into ${group.name} </h1>
    <i>no task recorded</i>
  </div>
% endif
