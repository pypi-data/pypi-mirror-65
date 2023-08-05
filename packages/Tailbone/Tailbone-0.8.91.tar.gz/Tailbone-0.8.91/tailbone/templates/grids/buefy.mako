## -*- coding: utf-8; -*-

<script type="text/x-template" id="grid-filter-date-value-template">
  <div class="level">
    <div class="level-left">
      <div class="level-item">
        <tailbone-datepicker v-model="startDate"
                             ref="startDate"
                             @input="startDateChanged">
        </tailbone-datepicker>
      </div>
      <div v-show="dateRange"
           class="level-item">
        and
      </div>
      <div v-show="dateRange"
           class="level-item">
        <tailbone-datepicker v-model="endDate"
                             ref="endDate"
                             @input="endDateChanged">
        </tailbone-datepicker>
      </div>
    </div>
  </div>
</script>

<script type="text/x-template" id="grid-filter-template">

  <div class="level filter" v-show="filter.visible">
    <div class="level-left">

      <div class="level-item filter-fieldname">

        <b-field>
          <b-checkbox-button v-model="filter.active" native-value="IGNORED">
            <b-icon pack="fas" icon="check" v-show="filter.active"></b-icon>
            <span>{{ filter.label }}</span>
          </b-checkbox-button>
        </b-field>

      </div>

      <b-field grouped v-show="filter.active" class="level-item">

        <b-select v-model="filter.verb"
                  @input="focusValue()"
                  class="filter-verb">
          <option v-for="verb in filter.verbs"
                  :key="verb"
                  :value="verb">
            {{ filter.verb_labels[verb] }}
          </option>
        </b-select>

        ## only one of the following "value input" elements will be rendered

        <grid-filter-date-value v-if="filter.data_type == 'date'"
                                v-model="filter.value"
                                v-show="valuedVerb()"
                                :date-range="filter.verb == 'between'"
                                ref="valueInput">
        </grid-filter-date-value>

        <b-select v-if="filter.data_type == 'choice'"
                  v-model="filter.value"
                  v-show="valuedVerb()"
                  ref="valueInput">
          <option v-for="choice in filter.choices"
                  :key="choice"
                  :value="choice">
            {{ filter.choice_labels[choice] || choice }}
          </option>
        </b-select>

        <b-input v-if="filter.data_type == 'string'"
                 v-model="filter.value"
                 v-show="valuedVerb()"
                 ref="valueInput">
        </b-input>

      </b-field>

    </div><!-- level-left -->
  </div><!-- level -->

</script>

<script type="text/x-template" id="tailbone-grid-template">
  <div>

    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5em;">

      <div style="display: flex; flex-direction: column; justify-content: space-between;">
        <div></div>
        <div class="filters">
          % if grid.filterable:
              ## TODO: stop using |n filter
              ${grid.render_filters(template='/grids/filters_buefy.mako', allow_save_defaults=allow_save_defaults)|n}
          % endif
        </div>
      </div>

      <div style="display: flex; flex-direction: column; justify-content: space-between;">

        <div class="context-menu">
          % if context_menu:
              <ul id="context-menu">
                ## TODO: stop using |n filter
                ${context_menu|n}
              </ul>
          % endif
        </div>

        <div class="grid-tools-wrapper">
          % if tools:
              <div class="grid-tools field is-grouped is-pulled-right">
                ## TODO: stop using |n filter
                ${tools|n}
              </div>
          % endif
        </div>

      </div>

    </div>

    <b-table
       :data="data"
       ## :columns="columns"
       :loading="loading"
       :row-class="getRowClass"

       :checkable="checkable"
       % if grid.checkboxes:
       :checked-rows.sync="checkedRows"
       % endif
       % if grid.check_handler:
       @check="${grid.check_handler}"
       % endif
       % if grid.check_all_handler:
       @check-all="${grid.check_all_handler}"
       % endif
       ## TODO: definitely will be wanting this...
       ## :is-row-checkable=""

       :default-sort="[sortField, sortOrder]"
       backend-sorting
       @sort="onSort"

       ## % if grid.pageable:
       ## paginated
       :paginated="paginated"
       :per-page="perPage"
       :current-page="currentPage"
       backend-pagination
       :total="total"
       @page-change="onPageChange"
       ## % endif

       ## TODO: should let grid (or master view) decide how to set these?
       icon-pack="fas"
       ## note that :striped="true" was interfering with row status (e.g. warning) styles
       :striped="false"
       :hoverable="true"
       :narrowed="true">

      <template slot-scope="props">
        % for column in grid_columns:
            <b-table-column field="${column['field']}" label="${column['label']}" ${'sortable' if column['sortable'] else ''}>
              % if grid.is_linked(column['field']):
                  <a :href="props.row._action_url_view" v-html="props.row.${column['field']}"></a>
              % else:
                  <span v-html="props.row.${column['field']}"></span>
              % endif
            </b-table-column>
        % endfor

        % if grid.main_actions or grid.more_actions:
            <b-table-column field="actions" label="Actions">
              % for action in grid.main_actions:
                  <a v-if="props.row._action_url_${action.key}"
                     :href="props.row._action_url_${action.key}"
                     class="grid-action${' has-text-danger' if action.key == 'delete' else ''}"
                     % if action.click_handler:
                     @click.prevent="${action.click_handler}"
                     % endif
                     >
                    <i class="fas fa-${action.icon}"></i>
                    ${action.label}
                  </a>
                  &nbsp;
              % endfor
            </b-table-column>
        % endif
      </template>

      <template slot="empty">
        <section class="section">
          <div class="content has-text-grey has-text-centered">
            <p>
              <b-icon
                 pack="fas"
                 icon="fas fa-sad-tear"
                 size="is-large">
              </b-icon>
            </p>
            <p>Nothing here.</p>
          </div>
        </section>
      </template>

      % if grid.pageable:
      <template slot="footer">
        <b-field grouped position="is-right"
                 v-if="firstItem">
          <span class="control">
            showing {{ firstItem.toLocaleString('en') }} - {{ lastItem.toLocaleString('en') }} of {{ total.toLocaleString('en') }} results;
          </span>
          <b-select v-model="perPage"
                    size="is-small"
                    @input="loadAsyncData()">
            % for value in grid.get_pagesize_options():
                <option value="${value}">${value}</option>
            % endfor
          </b-select>
          <span class="control">
            per page
          </span>
        </b-field>
      </template>
      % endif

    </b-table>
  </div>
</script>

<script type="text/javascript">

  let TailboneGridCurrentData = ${json.dumps(grid_data['data'])|n}

  let TailboneGridData = {
      loading: false,
      selectedFilter: null,
      ajaxDataUrl: ${json.dumps(grid.ajax_data_url)|n},

      data: TailboneGridCurrentData,
      rowStatusMap: ${json.dumps(grid_data['row_status_map'])|n},

      checkable: ${json.dumps(grid.checkboxes)|n},
      % if grid.checkboxes:
      checkedRows: ${grid_data['checked_rows_code']|n},
      % endif

      paginated: ${json.dumps(grid.pageable)|n},
      total: ${len(grid_data['data']) if static_data else grid_data['total_items']},
      perPage: ${json.dumps(grid.pagesize if grid.pageable else None)|n},
      currentPage: ${json.dumps(grid.page if grid.pageable else None)|n},
      firstItem: ${json.dumps(grid_data['first_item'] if grid.pageable else None)|n},
      lastItem: ${json.dumps(grid_data['last_item'] if grid.pageable else None)|n},

      sortField: ${json.dumps(grid.sortkey if grid.sortable else None)|n},
      sortOrder: ${json.dumps(grid.sortdir if grid.sortable else None)|n},

      ## filterable: ${json.dumps(grid.filterable)|n},
      filters: ${json.dumps(filters_data if grid.filterable else None)|n},
      filtersSequence: ${json.dumps(filters_sequence if grid.filterable else None)|n},
      selectedFilter: null,
  }

</script>
