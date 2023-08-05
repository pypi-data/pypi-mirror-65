<%def name="publish_projects_list(projects_list)">
  % if projects_list :
    <!-- Single button for project management-->
    <div class="btn-group">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
        % if project is not UNDEFINED and project is not None and len(project.groups)>0:
          <span id="project_name">${project.groups[0].name}</span> <span class="caret"></span>
        % elif project is not UNDEFINED and project is not None:
          <span id="project_name">${project.name}</span> <span class="caret"></span>
        % else :
          Projects (<span id="project_number">${len(projects_list)}</span>)<span class="caret"></span>
        % endif
      </button>
      <ul id="projects_list" class="dropdown-menu" role="menu" data-url="${url(route_name='project_edit',id='')}">
      <%
        groups_list=sorted({_p.groups[0] for _p in projects_list if len(_p.groups)!=0}, key=lambda group: group.name)
        none_affected_projects = [_p for _p in projects_list if len(_p.groups)==0]
      %>
      % if len(groups_list)>0 :
        ## check there's at least one group
        <li>Groups</li>
        % for __group in groups_list :
        <li><a class="project_link" href="${url(route_name='project_group_view', id=__group.id)}">${__group.name}</a></li>
        % endfor
        <li class="divider"></li>
      % endif
      % if len(none_affected_projects)>0 :
        ## check there's at least one project :/
        <li>Projects</li>
      % endif
      % for __project in none_affected_projects :
        <li><a class="project_link" href="${url(route_name='project_edit',id=__project.id)}">${__project.name}</a></li>
      % endfor
      % if ((project is UNDEFINED or project is None) and request.url == request.route_path('home')) or project is not UNDEFINED:
        <li class="divider"></li>
        <li><a href="#" onclick="$('#new_project_dialog').modal('show');">Add a new project</a></li>
       % endif
      </ul>
    </div>
  % else :
    <!-- Single button for project management-->
    <div class="btn-group" style="display:none">
      <button type="button" class="btn btn-default dropdown-toggle" data-toggle="dropdown">
          Projects (<span id="project_number">0</span>) <span class="caret"></span>
      </button>
      <ul id="projects_list" class="dropdown-menu" role="menu" data-url="${url(route_name='project_edit',id='')}">
      </ul>
    </div>
  % endif
</%def>

<%def name="publish_new_branch_dialog()">
  <div id="confirm_force_push_dialog" class="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
          <h4 class="modal-title">It seems you are trying to push a new branch.</h4>
        </div>
        <div class="modal-body">
          Should we push also it ?
        </div>
        <div class="modal-footer">
          <button id="abort_new_branch" type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          <button id="new_branch" type="button" class="btn btn-primary">Push this new branch</button>
        </div>
      </div><!-- /.modal-content -->
    </div><!-- /.modal-dialog -->
  </div><!-- /.modal -->
</%def>

<%def name="publish_project_dialog()">
  <div id="new_project_dialog" class="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
          <h4 class="modal-title">Add a new project</h4>
        </div>
        <div class="modal-body">
          <form id="project_add" name="project_add" action="${url('project_add')}" method="post" class="form-horizontal" role="form">
            <div id="new_project">
                <div class="form-group">
                  <label for="new_project_name" class="col-sm-2 control-label">Name</label>
                  <div class="col-sm-8">
                    <input id="new_project_name" class="form-control" name="name" type="text" placeholder="name">
                  </div>
                </div>
                <div class="form-group">
                  <label for="new_project_host" class="col-sm-2 control-label">Host</label>
                  <div class="col-sm-8">
                    <input id="new_project_host" class="form-control" name="host" type="text" placeholder="hostname">
                  </div>
                </div>
                <div class="form-group">
                  <label for="new_project_path" class="col-sm-2 control-label">Folder</label>
                  <div class="col-sm-8">
                    <input id="new_project_path" class="form-control" name="path" type="text" placeholder="/home/sites ...">
                  </div>
                </div>
                <div class="form-group">
                  <label for="new_project_group_label" class="col-sm-2 control-label">Group</label>
                  <div class="col-sm-8">
                    <input id="group_label" class="form-control typeahead" style="width:20em" name="group_label" type="text" placeholder="add your project into a group" value="">
                  </div>
                </div>
                <div class="form-group">
                  <label for="new_project_user" class="col-sm-2 control-label">User</label>
                  <div class="col-sm-8">
                    <input id="new_project_user" class="form-control" name="user" type="text" placeholder="user">
                  </div>
                </div>
                <div class="form-group">
                  <label for="new_project_password" class="col-sm-2 control-label">Passwd</label>
                  <div class="col-sm-8">
                    <input id="new_project_password" class="form-control" name="password" type="password" placeholder="password">
                    <input name="dashboard" type="hidden" value="0">
                    <input name="no_scan" type="hidden" value="0">
                    <input name="rev_init" type="hidden" value="0">
                    <input name="dvcs_release" type="hidden" value="">
                  </div>
                </div>
                <div class="form-group">
                  <label for="project_scan" class="col-sm-2 control-label">PKEY</label>
                  <div class="col-sm-8">
                    <div class="checkbox">
                      <label>
                          <input name="local_pkey" type="checkbox" value="1" onclick="$('#project_add input[type=password]').prop('disabled', $(this).is(':checked'))">
                      </label>
                    </div>
                  </div>
                </div>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button id="cancel_add_project" type="button" class="btn btn-default" data-dismiss="modal">Close</button>
          <button id="add_my_project" type="button" class="btn btn-primary" onclick="add_project('${url('project_add')}', '${url('projects_list_global')}');">Save changes</button>
        </div>
      </div><!-- /.modal-content -->
    </div><!-- /.modal-dialog -->
  </div><!-- /.modal -->
</%def>


<%def name="publish_user_dialog()">
<div id="new_user_dialog" class="modal">
  <div class="modal-dialog">
    <div class="modal-content">

      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Add a new user</h4>
      </div><!-- /.modal-header -->

      <div class="modal-body">
        <form id="user" name="user" action="${url('user_add')}" method="post" class="form-horizontal" role="form">
          <div id="new_user">
              <div class="form-group">
                <label for="new_user_name" class="col-sm-2 control-label">Full name</label>
                <div class="col-sm-8">
                  <input id="new_user_name" class="form-control" name="name" type="text" placeholder="name">
                </div>
              </div>
              <div class="form-group">
                <label for="new_user_name" class="col-sm-2 control-label">Email</label>
                <div class="col-sm-8">
                  <input id="new_user_email" class="form-control" name="email" type="text" placeholder="email">
                </div>
              </div>
              <div class="form-group">
                <label for="new_user_password" class="col-sm-2 control-label">Passwd</label>
                <div class="col-sm-8">
                  <input id="new_user_password" class="form-control" name="pwd" type="password" placeholder="password">
                </div>
              </div>
          </div>
        </form>
      </div><!-- /.modal-body -->

      <div class="modal-footer">
        <button id="cancel_add_user" type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="add_my_user" type="button" class="btn btn-primary" onclick="add_user('${url('user_add')}');">Save changes</button>
      </div><!-- /.modal-footer -->

    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
</%def>

<%def name="publish_update_user_dialog()">
<div id="update_user_dialog" class="modal">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title">Update user</h4>
      </div>
      <div class="modal-body">
        <form id="update_user_form" name="user" action="" method="post" class="form-horizontal" role="form">
          <div id="update_user">
              <div class="form-group">
                <label for="udate_user_name" class="col-sm-2 control-label">Full name</label>
                <div class="col-sm-8">
                  <input id="update_user_name" class="form-control" name="name" type="text" placeholder="name">
                </div>
              </div>
              <div class="form-group">
                <label for="update_user_name" class="col-sm-2 control-label">Email</label>
                <div class="col-sm-8">
                  <input id="update_user_email" class="form-control" name="email" type="text" placeholder="email">
                </div>
              </div>
              <div class="form-group">
                <label for="update_user_password" class="col-sm-2 control-label">Passwd</label>
                <div class="col-sm-8">
                  <input id="update_user_password" class="form-control" name="pwd" type="password" placeholder="password">
                </div>
              </div>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button id="cancel_update_user" type="button" class="btn btn-default" data-dismiss="modal">Close</button>
        <button id="update_my_user" type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div><!-- /.modal-content -->
  </div><!-- /.modal-dialog -->
</div><!-- /.modal -->
</%def>
