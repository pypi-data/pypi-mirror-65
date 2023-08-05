<%!
  import json
  import os.path
%>
<%inherit file="base.mako"/>
<%namespace name="lib" file="lib.mako"/>
  <h2>
        <span class="label label-default">User management</span>
        <button style="background-color:transparent;border:none" onclick="$('#new_user_dialog').modal('show');" alt="add a user">
          <span class='glyphicon glyphicon-plus' style="font-size:26px;vertical-align:bottom"></span>
        </button>
  </h2>
  <%
     user_table_display=''
  %>
  
  % if len(lst_users)==0 and len(projects_list)>0 :
     <%
        user_table_display='display:none'
     %>
    <div class="missing">
        <h3><i>Please define users in order to link them to a project</i></h3>
    </div>
  % else :
    <div>
        <h3><i>Please create user and project first</i></h3>
    </div>
  % endif
  <div id="overview" class="panel panel-default" style="${user_table_display}">
    <div>
       <p class="bg-info" style="padding:5px">
         Your list of users
       </p>
    </div>
    <div>
       <!-- project compare table -->
       <table id="users_overview" class="table table-condensed" data-update_url="${url('users_json')}">
          <thead>
            <th>Name</th>
            <th>Email (a.k.a. login)</th>
            <th>Creation date</th>
            <th>&nbsp;</th>
            <th>&nbsp;</th>
            <th>&nbsp;</th>
          </thead>
          <tbody>
            % for user in lst_users :
               <tr>
                  <td>${user.name}</td>
                  <td>${user.email}</td>
                  <td>${user.creation_date.strftime('%d/%m/%Y %H:%M')}</td>
                  <td><button class="btn btn-default" onclick="edit_user_acl(this, ${user.id})">edit user acl</button></td>
                  <td><button class="btn btn-default" onclick="edit_user('${url('user_update', id=user.id)}', '${url('user_get', id=user.id)}', '${user.id}')">edit user properties</button></td>
                  <td><button class="btn btn-default" onclick="go_to('${url('user_delete', id=user.id)}')">delete</button></td>
               </tr>
            % endfor
            % if not lst_users :
               <tr>
                  <td colspan="5" style="text-align:center;padding-top:20px">No Users defined</td>
               </tr>
            % endif :
          </tbody>
       </table>
    </div>
  </div>

  <!-- small global overview to manage all your user ACE instead of setting them
     project by project -->
  <h2>
        <span class="label label-default">Acls management</span>
  </h2>

  % if len(lst_users)>0 and len(projects_list)>0 :
  <div id="overview" class="panel panel-default">
    <div>
       <p class="bg-info" style="padding:5px">
         Your ACLs
       </p>
    </div>
    <div>
     <form name="users_acls" id="users_acls" action="${url(route_name='users_save_acls')}" method="post">
       <!-- project compare table -->
       <%
         _chunks_users = [lst_users[x:x+6] for x in range(0,len(lst_users),6)]
       %>
       % for _chunk_users in _chunks_users :
         <table class="acls_overview table table-condensed" data-update_url="${url('users_json')}">
            <thead>
              <th>Projects</th>
              % for i, user in enumerate(_chunk_users) :
                 <th data-user_id="${user.id}" class="user_head_class"> ${user.name} </th>
                 % if i==2:
                  <th class="extra_col_project">Projects</th>
                 % endif
              % endfor
            </thead>
            <tbody>
               % for __project in projects_list :
                 <tr>
                    <td>${__project.name}</td>
                    % for i, user in enumerate(_chunk_users) :
                      <td>
                       <select name="${__project.id}__${user.id}" class="ace" data-project_id="${__project.id}" data-user_id="${user.id}">
                         <option value=""> ----- </option>
                         % for acl_label in known_acls :
                             % if project_acls[__project.id].get(user.id) == acl_label :
                               <option value="${acl_label}" selected>${acl_label}</option>
                             % else :
                               <option value="${acl_label}">${acl_label}</option>
                             % endif
                         % endfor
                       </select>
                      </td>
                      % if i==2:
                        <td class="extra_col_project">${__project.name}</td>
                      % endif
                    % endfor
                 </tr>
               % endfor
            </tbody>
         </table>
       % endfor

       <button id="save_users_acl" class="btn btn-primary" onclick="save_project_acls()">Save your modifications</button>
       <br>
       <br>
     </form>
    </div>
  </div>
  % elif len(lst_users)>0 and len(projects_list)==0 :
    <div>
        <h3><i>No ACLs can be defined. Please define a project in order to link a user profile to a project</i></h3>
    </div>
  % else :
    <div>
        <h3><i>No ACLs can be defined. Please create user and project first</i></h3>
    </div>
  % endif

${lib.publish_user_dialog()}
${lib.publish_update_user_dialog()}

