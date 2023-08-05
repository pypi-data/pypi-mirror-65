## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.batch.js') + '?ver={}'.format(tailbone.__version__))}
  <script type="text/javascript">

    var has_execution_options = ${'true' if master.has_execution_options(batch) else 'false'};

    $(function() {
        % if master.has_worksheet:
            $('.load-worksheet').click(function() {
                disable_button(this);
                location.href = '${url('{}.worksheet'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
        % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
            $('#refresh-data').click(function() {
                $(this)
                    .button('option', 'disabled', true)
                    .button('option', 'label', "Working, please wait...");
                location.href = '${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}';
            });
        % endif
    });

  </script>
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if not use_buefy:
  <style type="text/css">

    .grid-wrapper {
        margin-top: 10px;
    }

    .complete form {
        display: inline;
    }
    
  </style>
  % endif
</%def>

<%def name="buttons()">
    <div class="buttons">
      ${self.leading_buttons()}
      ${refresh_button()}
    </div>
</%def>

<%def name="leading_buttons()">
  % if master.has_worksheet and master.allow_worksheet(batch) and request.has_perm('{}.worksheet'.format(permission_prefix)):
      <button type="button" class="load-worksheet">Edit as Worksheet</button>
  % endif
</%def>

<%def name="refresh_button()">
  % if master.batch_refreshable(batch) and request.has_perm('{}.refresh'.format(permission_prefix)):
      % if use_buefy:
          ## TODO: this should surely use a POST request?
          <once-button tag="a"
                       href="${url('{}.refresh'.format(route_prefix), uuid=batch.uuid)}"
                       text="Refresh Data">
          </once-button>
      % else:
          <button type="button" class="button" id="refresh-data">Refresh Data</button>
      % endif
  % endif
</%def>

<%def name="execute_submit_button()">
  <b-button type="is-primary"
            % if master.has_execution_options(batch):
            @click="executeBatch"
            % else:
            native-type="submit"
            % endif
            % if not execute_enabled:
            disabled
            % elif not master.has_execution_options(batch):
            :disabled="executeFormSubmitting"
            % endif
            % if why_not_execute:
            title="${why_not_execute}"
            % endif
            >
    % if master.has_execution_options(batch):
    ${execute_title}
    % else:
    {{ executeFormButtonText }}
    % endif
  </b-button>
</%def>

<%def name="object_helpers()">
  ${self.render_status_breakdown()}
  ${self.render_execute_helper()}
</%def>

<%def name="render_status_breakdown()">
  % if status_breakdown is not Undefined and status_breakdown is not None:
      <div class="object-helper">
        <h3>Row Status Breakdown</h3>
        <div class="object-helper-content">
          % if use_buefy:
              ${status_breakdown_grid.render_buefy_table_element(data_prop='statusBreakdownData', empty_labels=True)|n}
          % elif status_breakdown:
              <div class="grid full">
                <table>
                  % for i, (status, count) in enumerate(status_breakdown):
                      <tr class="${'even' if i % 2 == 0 else 'odd'}">
                        <td>${status}</td>
                        <td>${count}</td>
                      </tr>
                  % endfor
                </table>
              </div>
          % else:
              <p>Nothing to report yet.</p>
          % endif
        </div>
      </div>
  % endif
</%def>

<%def name="render_execute_helper()">
  <div class="object-helper">
    <h3>Batch Execution</h3>
    <div class="object-helper-content">
      % if batch.executed:
          <p>
            Batch was executed
            ${h.pretty_datetime(request.rattail_config, batch.executed)}
            by ${batch.executed_by}
          </p>
      % elif master.handler.executable(batch):
          % if request.has_perm('{}.execute'.format(permission_prefix)):
              <p>Batch has not yet been executed.</p>
              % if use_buefy:
                  % if master.has_execution_options(batch):
                      <p>TODO: must implement execution with options</p>
                  % else:
                      <execute-form></execute-form>
                  % endif
              % else:
                  ## no buefy, do legacy thing
                  <button type="button"
                          % if not execute_enabled:
                          disabled="disabled"
                          % endif
                          % if why_not_execute:
                          title="${why_not_execute}"
                          % endif
                          class="button is-primary"
                          id="execute-batch">
                    ${execute_title}
                  </button>
              % endif
          % else:
              <p>TODO: batch *may* be executed, but not by *you*</p>
          % endif
      % else:
          <p>TODO: batch cannot be executed..?</p>
      % endif
    </div>
  </div>
</%def>

<%def name="render_form()">
  ## TODO: should use self.render_form_buttons()
  ## ${form.render(form_id='batch-form', buttons=capture(self.render_form_buttons))|n}
  ${form.render(form_id='batch-form', buttons=capture(buttons))|n}
</%def>

<%def name="render_this_page()">
  ${parent.render_this_page()}
  % if not use_buefy:
      % if master.handler.executable(batch) and request.has_perm('{}.execute'.format(permission_prefix)):
          <div id="execution-options-dialog" style="display: none;">
            ${execute_form.render_deform(form_kwargs={'name': 'batch-execution'}, buttons=False)|n}
          </div>
      % endif
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}
  % if use_buefy and master.handler.executable(batch) and request.has_perm('{}.execute'.format(permission_prefix)):
      ## TODO: stop using |n filter
      ${execute_form.render_deform(buttons=capture(execute_submit_button), form_kwargs={'@submit': 'submitExecuteForm'})|n}
  % endif
</%def>

<%def name="modify_this_page_vars()">
  ${parent.modify_this_page_vars()}
  <script type="text/javascript">

    ThisPageData.statusBreakdownData = ${json.dumps(status_breakdown_grid.get_buefy_data()['data'])|n}

  </script>

  % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
      <script type="text/javascript">

        ${execute_form.component_studly}Data.executeFormButtonText = "${execute_title}"
        ${execute_form.component_studly}Data.executeFormSubmitting = false

        ${execute_form.component_studly}.methods.executeBatch = function() {
            alert("TODO: implement options dialog for batch execution")
        }

        ${execute_form.component_studly}.methods.submitExecuteForm = function() {
            this.executeFormSubmitting = true
            this.executeFormButtonText = "Executing, please wait..."
        }

      </script>
  % endif
</%def>

<%def name="finalize_this_page_vars()">
  ${parent.finalize_this_page_vars()}
  % if not batch.executed and request.has_perm('{}.execute'.format(permission_prefix)):
      <script type="text/javascript">

        ${execute_form.component_studly}.data = function() { return ${execute_form.component_studly}Data }

        Vue.component('${execute_form.component}', ${execute_form.component_studly})

      </script>
  % endif
</%def>


${parent.body()}
