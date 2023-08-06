<%!
  import json
%>
<%inherit file="base.mako"/>
<%namespace name="lib" file="lib.mako"/>

% if logged_in is not None :
  <h2>
        <span class="label label-default">Dashboard</span>

        % if logged_in is not None and request.registry.settings['hg_delivery.default_login'] == request.authenticated_userid:
        <button type="button" style="background-color:transparent;border:none" onclick="$('#new_project_dialog').modal('show');" alt="add new project">
          <span class='glyphicon glyphicon-plus' style="font-size:26px;vertical-align:bottom"></span>
        </button>
        % endif
  </h2>
  %for project in dashboard_list :
    <div class="panel panel-default node_description" data-id="${project.id}" data-update_url="${url(route_name='description',id=project.id)}">
      <div class="panel-heading">
        <h3 class="panel-title">
          <a href="${url(route_name='project_edit',id=project.id)}"><b>${project.name}</b></a>
          <i>(revision : <span class='node_description_rev'></span>)</i>
          
        </h3>
      </div>
      <div class="panel-body">
        current branch : <span class="label label-warning node_description_branch"></span
        <br>
        <br>
        current hash : <i><span class='node_description_node'></span></i>
        <br>
        current comment : <i><span class='node_description_desc'></span></i>
      </div>
    </div>
  %endfor
  %if not dashboard_list :
      > <i>The dashboard is empty</i>
  %endif

% else :

 <div class="starter-template">
   <h1>Welcome to HgDelivery webapp</h1>
   <p class="lead">The purpose of HgDelivery webapp is to allow people to deliver or manage new release easily</p>
   <br>
   <br>
   <p class="lead"><b>Please login before proceeding</b></p>
   <br>
   % if logged_in is None :
   <div>
       <form id="login_form_responsive" action="${url('login')}" method='POST'>
         <input class="span2" name="login" type="text" placeholder="your mail address">
         <input class="span2" name="password" type="password" placeholder="your password">
         <button type="submit" class="btn btn-primary" onclick="$('#login_form').submit()">Sign in</button>
       </form>
   </div>
 </div>

 %endif

% endif

% if logged_in is not None :
   ${lib.publish_project_dialog()}
% endif

<%block name="local_js">
  <script>
  % if logged_in is not None :
     var groups_labels = ${json.dumps(list({_p.groups[0].name for _p in projects_list if len(_p.groups)!= 0}))|n};
  % else :
     var groups_labels = [];
  % endif
  init_page_overview();

  if(typeof(URLSearchParams)!=='undefined'){
    var url_params = new URLSearchParams(window.location.search);
    if(url_params.get('error')!==null && url_params.get('error')!==''){
      _alert_html = '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>';
      if(url_params.get('message')!==null && url_params.get('message')!==''){
        _alert_html += url_params.get('message') + ':' + '&nbsp;';
      }
      _alert_html += '<strong>'+url_params.get('error')+'</strong></div>';
      $('#container_alert').html(_alert_html);
    }
  } else {
    var url_params = window.location.search.substr(1).split('&').reduce(function (q, query) {
      var chunks = query.split('=');
      var key = chunks[0];
      var value = chunks[1];
      return (q[key] = value, q);
    }, {});
    if(typeof(url_params['error'])!=='undefined' && url_params['error']!==null && url_params['error']!==''){
      _alert_html = '<div class="alert alert-danger"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>';
      if(url_params['message']!==null && url_params['message']!==''){
        _alert_html += url_params['message'].replace('+',' ') + ':' + '&nbsp;';
      }
      _alert_html += '<strong>'+url_params['error'].replace('+',' ')+'</strong></div>';
      $('#container_alert').html(_alert_html);
    }
  }


  </script>
</%block>


