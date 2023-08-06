## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />

<%def name="page_content()">
  <profile-info></profile-info>
</%def>

<%def name="render_this_page()">
  ${self.page_content()}
</%def>

<%def name="render_member_tab()">
  <b-tab-item label="Member" icon-pack="fas" :icon="members.length ? 'check' : null">

    <div v-if="members.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} is associated with <strong>{{ members.length }}</strong> member account(s)</p>
      </div>

      <br />
      <b-collapse v-for="member in members"
                  :key="member.uuid"
                  class="panel"
                  :open="members.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>#{{ member.number }} {{ member.display }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="Number">
                {{ member.number }}
              </b-field>

              <b-field horizontal label="ID">
                {{ member.id }}
              </b-field>

              <b-field horizontal label="Active">
                {{ member.active }}
              </b-field>

              <b-field horizontal label="Joined">
                {{ member.joined }}
              </b-field>

              <b-field horizontal label="Withdrew"
                       v-if="member.withdrew">
                {{ member.withdrew }}
              </b-field>

              <b-field horizontal label="Person">
                <a v-if="member.person_uuid != person.uuid"
                   :href="member.view_profile_url">
                  {{ member.person_display_name }}
                </a>
                <span v-if="member.person_uuid == person.uuid">
                  {{ member.person_display_name }}
                </span>
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_member_panel_buttons(member)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!members.length">
      <p>{{ person.display_name }} has never had a member account.</p>
    </div>

  </b-tab-item>
</%def>

<%def name="render_member_panel_buttons(member)">
  % if request.has_perm('members.view'):
      <b-button tag="a" :href="member.view_url">
        View Member
      </b-button>
  % endif
</%def>

<%def name="render_customer_tab()">
  <b-tab-item label="Customer" icon-pack="fas" :icon="customers.length ? 'check' : null">

    <div v-if="customers.length">

      <div style="display: flex; justify-content: space-between;">
        <p>{{ person.display_name }} is associated with <strong>{{ customers.length }}</strong> customer account(s)</p>
      </div>

      <br />
      <b-collapse v-for="customer in customers"
                  :key="customer.uuid"
                  class="panel"
                  :open="customers.length == 1">

        <div slot="trigger"
             slot-scope="props"
             class="panel-heading"
             role="button">
          <b-icon pack="fas"
                  icon="caret-right">
          </b-icon>
          <strong>#{{ customer.number }} {{ customer.name }}</strong>
        </div>

        <div class="panel-block">
          <div style="display: flex; justify-content: space-between; width: 100%;">
            <div style="flex-grow: 1;">

              <b-field horizontal label="Number">
                {{ customer.number }}
              </b-field>

              <b-field horizontal label="ID">
                {{ customer.id }}
              </b-field>

              <b-field horizontal label="Name">
                {{ customer.name }}
              </b-field>

              <b-field horizontal label="People">
                <ul>
                  <li v-for="p in customer.people"
                      :key="p.uuid">
                    <a v-if="p.uuid != person.uuid"
                       :href="p.view_profile_url">
                      {{ p.display_name }}
                    </a>
                    <span v-if="p.uuid == person.uuid">
                      {{ p.display_name }}
                    </span>
                  </li>
                </ul>
              </b-field>

              <b-field horizontal label="Address"
                       v-for="address in customer.addresses"
                       :key="address.uuid">
                {{ address.display }}
              </b-field>

            </div>
            <div class="buttons" style="align-items: start;">
              ${self.render_customer_panel_buttons(customer)}
            </div>
          </div>
        </div>
      </b-collapse>
    </div>

    <div v-if="!customers.length">
      <p>{{ person.display_name }} has never had a customer account.</p>
    </div>

  </b-tab-item> <!-- Customer -->
</%def>

<%def name="render_customer_panel_buttons(customer)">
  % if request.has_perm('customers.view'):
      <b-button tag="a" :href="customer.view_url">
        View Customer
      </b-button>
  % endif
</%def>

<%def name="render_this_page_template()">
  ${parent.render_this_page_template()}

  <script type="text/x-template" id="profile-info-template">
    <div>
      <b-tabs v-model="activeTab" type="is-boxed">

        <b-tab-item label="Personal" icon="check" icon-pack="fas">
          <div style="display: flex; justify-content: space-between;">

            <div>

              <div class="field-wrapper first_name">
                <div class="field-row">
                  <label>First Name</label>
                  <div class="field">
                    ${person.first_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper middle_name">
                <div class="field-row">
                  <label>Middle Name</label>
                  <div class="field">
                    ${person.middle_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper last_name">
                <div class="field-row">
                  <label>Last Name</label>
                  <div class="field">
                    ${person.last_name}
                  </div>
                </div>
              </div>

              <div class="field-wrapper street">
                <div class="field-row">
                  <label>Street 1</label>
                  <div class="field">
                    ${person.address.street if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper street2">
                <div class="field-row">
                  <label>Street 2</label>
                  <div class="field">
                    ${person.address.street2 if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper city">
                <div class="field-row">
                  <label>City</label>
                  <div class="field">
                    ${person.address.city if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper state">
                <div class="field-row">
                  <label>State</label>
                  <div class="field">
                    ${person.address.state if person.address else ''}
                  </div>
                </div>
              </div>

              <div class="field-wrapper zipcode">
                <div class="field-row">
                  <label>Zipcode</label>
                  <div class="field">
                    ${person.address.zipcode if person.address else ''}
                  </div>
                </div>
              </div>

              % if person.phones:
                  % for phone in person.phones:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Phone Number</label>
                          <div class="field">
                            ${phone.number} (type: ${phone.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Phone Number</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

              % if person.emails:
                  % for email in person.emails:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Email Address</label>
                          <div class="field">
                            ${email.address} (type: ${email.type})
                          </div>
                        </div>
                      </div>
                  % endfor
              % else:
                  <div class="field-wrapper">
                    <div class="field-row">
                      <label>Email Address</label>
                      <div class="field">
                        (none on file)
                      </div>
                    </div>
                  </div>
              % endif

            </div>

            <div>
              % if request.has_perm('people.view'):
                  ${h.link_to("View Person", url('people.view', uuid=person.uuid), class_='button')}
              % endif
            </div>

          </div>
        </b-tab-item><!-- Personal -->

        ${self.render_customer_tab()}

        ${self.render_member_tab()}

        <b-tab-item label="Employee" ${'icon="check" icon-pack="fas"' if employee else ''|n}>

          % if employee:
              <div style="display: flex; justify-content: space-between;">

                <div>

                  <div class="field-wrapper id">
                    <div class="field-row">
                      <label>ID</label>
                      <div class="field">
                        ${employee.id or ''}
                      </div>
                    </div>
                  </div>

                  <div class="field-wrapper display_name">
                    <div class="field-row">
                      <label>Display Name</label>
                      <div class="field">
                        ${employee.display_name or ''}
                      </div>
                    </div>
                  </div>

                  <div class="field-wrapper status">
                    <div class="field-row">
                      <label>Status</label>
                      <div class="field">
                        ${enum.EMPLOYEE_STATUS.get(employee.status, '')}
                      </div>
                    </div>
                  </div>

                  % if employee.phones:
                      % for phone in employee.phones:
                          <div class="field-wrapper">
                            <div class="field-row">
                              <label>Phone Number</label>
                              <div class="field">
                                ${phone.number} (type: ${phone.type})
                              </div>
                            </div>
                          </div>
                      % endfor
                  % else:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Phone Number</label>
                          <div class="field">
                            (none on file)
                          </div>
                        </div>
                      </div>
                  % endif

                  % if employee.emails:
                      % for email in employee.emails:
                          <div class="field-wrapper">
                            <div class="field-row">
                              <label>Email Address</label>
                              <div class="field">
                                ${email.address} (type: ${email.type})
                              </div>
                            </div>
                          </div>
                      % endfor
                  % else:
                      <div class="field-wrapper">
                        <div class="field-row">
                          <label>Email Address</label>
                          <div class="field">
                            (none on file)
                          </div>
                        </div>
                      </div>
                  % endif

                </div>

                <div>
                  % if request.has_perm('employees.view'):
                      ${h.link_to("View Employee", url('employees.view', uuid=employee.uuid), class_='button')}
                  % endif
                </div>

              </div>

          % else:
              <p>${person} has never been an employee.</p>
          % endif
        </b-tab-item><!-- Employee -->

        <b-tab-item label="User" ${'icon="check" icon-pack="fas"' if person.users else ''|n}>
          % if person.users:
              <p>${person} is associated with <strong>${len(person.users)}</strong> user account(s)</p>
              <br />
              <div id="users-accordion">
                % for user in person.users:

                    <b-collapse class="panel"
                                ## TODO: what's up with aria-id here?
                                ## aria-id="contentIdForA11y2"
                                >

                      <div
                         slot="trigger"
                         class="panel-heading"
                         role="button"
                         ## TODO: what's up with aria-id here?
                         ## aria-controls="contentIdForA11y2"
                         >
                        <strong>${user.username}</strong>
                      </div>

                      <div class="panel-block">

                        <div style="display: flex; justify-content: space-between; width: 100%;">

                          <div>

                            <div class="field-wrapper id">
                              <div class="field-row">
                                <label>Username</label>
                                <div class="field">
                                  ${user.username}
                                </div>
                              </div>
                            </div>

                          </div>

                          <div>
                            % if request.has_perm('users.view'):
                                ${h.link_to("View User", url('users.view', uuid=user.uuid), class_='button')}
                            % endif
                          </div>

                        </div>

                      </div>
                    </b-collapse>
                % endfor
              </div>

          % else:
              <p>${person} has never been a user.</p>
          % endif
        </b-tab-item><!-- User -->

      </b-tabs>
    </div>
  </script>
</%def>

<%def name="make_this_page_component()">
  ${parent.make_this_page_component()}
  <script type="text/javascript">

    const ProfileInfo = {
        template: '#profile-info-template',
        data() {
            return {
                activeTab: 0,
                person: ${json.dumps(person_data)|n},
                customers: ${json.dumps(customers_data)|n},
                members: ${json.dumps(members_data)|n},
            }
        },
    }

    Vue.component('profile-info', ProfileInfo)

  </script>
</%def>


${parent.body()}
