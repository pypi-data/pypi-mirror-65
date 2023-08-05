
const GridFilterDateValue = {
    template: '#grid-filter-date-value-template',
    props: {
        value: String,
        dateRange: Boolean,
    },
    data() {
        return {
            startDate: null,
            endDate: null,
        }
    },
    mounted() {
        if (this.dateRange) {
            if (this.value.includes('|')) {
                let values = this.value.split('|')
                if (values.length == 2) {
                    this.startDate = values[0]
                    this.endDate = values[1]
                } else {
                    this.startDate = this.value
                }
            } else {
                this.startDate = this.value
            }
        } else {
            this.startDate = this.value
        }
    },
    methods: {
        focus() {
            this.$refs.startDate.focus()
        },
        startDateChanged(value) {
            if (this.dateRange) {
                value += '|' + this.endDate
            }
            this.$emit('input', value)
        },
        endDateChanged(value) {
            value = this.startDate + '|' + value
            this.$emit('input', value)
        },
    },
}

Vue.component('grid-filter-date-value', GridFilterDateValue)


const GridFilter = {
    template: '#grid-filter-template',
    props: {
        filter: Object
    },

    methods: {

        changeVerb() {
            // set focus to value input, "as quickly as we can"
            this.$nextTick(function() {
                this.focusValue()
            })
        },

        valuedVerb() {
            /* this returns true if the filter's current verb should expose value input(s) */

            // if filter has no "valueless" verbs, then all verbs should expose value inputs
            if (!this.filter.valueless_verbs) {
                return true
            }

            // if filter *does* have valueless verbs, check if "current" verb is valueless
            if (this.filter.valueless_verbs.includes(this.filter.verb)) {
                return false
            }

            // current verb is *not* valueless
            return true
        },

        focusValue: function() {
            this.$refs.valueInput.focus()
            // this.$refs.valueInput.select()
        }
    }
}

Vue.component('grid-filter', GridFilter)


let TailboneGrid = {
    template: '#tailbone-grid-template',

    props: {
        csrftoken: String,
    },

    computed: {
        // note, can use this with v-model for hidden 'uuids' fields
        selected_uuids: function() {
            return this.checkedRowUUIDs().join(',')
        },
    },

    methods: {

        getRowClass(row, index) {
            return this.rowStatusMap[index]
        },

        loadAsyncData(params) {

            if (params === undefined) {
                params = [
                    'partial=true',
                    `sortkey=${this.sortField}`,
                    `sortdir=${this.sortOrder}`,
                    `pagesize=${this.perPage}`,
                    `page=${this.page}`
                ].join('&')
            }

            this.loading = true
            this.$http.get(`${this.ajaxDataUrl}?${params}`).then(({ data }) => {
                TailboneGridCurrentData = data.data
                this.data = TailboneGridCurrentData
                this.rowStatusMap = data.row_status_map
                this.total = data.total_items
                this.firstItem = data.first_item
                this.lastItem = data.last_item
                this.loading = false
                this.checkedRows = this.locateCheckedRows(data.checked_rows)
            })
            .catch((error) => {
                this.data = []
                this.total = 0
                this.loading = false
                throw error
            })
        },

        locateCheckedRows(checked) {
            let rows = []
            if (checked) {
                for (let i = 0; i < this.data.length; i++) {
                    if (checked.includes(i)) {
                        rows.push(this.data[i])
                    }
                }
            }
            return rows
        },

        onPageChange(page) {
            this.page = page
            this.loadAsyncData()
        },

        onSort(field, order) {
            this.sortField = field
            this.sortOrder = order
            // always reset to first page when changing sort options
            // TODO: i mean..right? would we ever not want that?
            this.page = 1
            this.loadAsyncData()
        },

        resetView() {
            this.loading = true
            location.href = '?reset-to-default-filters=true'
        },

        addFilter(filter_key) {

            // reset dropdown so user again sees "Add Filter" placeholder
            this.$nextTick(function() {
                this.selectedFilter = null
            })

            // show corresponding grid filter
            this.filters[filter_key].visible = true
            this.filters[filter_key].active = true

            // track down the component
            var gridFilter = null
            for (var gf of this.$refs.gridFilters) {
                if (gf.filter.key == filter_key) {
                    gridFilter = gf
                    break
                }
            }

            // tell component to focus the value field, ASAP
            this.$nextTick(function() {
                gridFilter.focusValue()
            })

        },

        applyFilters(params) {
            if (params === undefined) {
                params = []
            }

            params.push('partial=true')
            params.push('filter=true')

            for (var key in this.filters) {
                var filter = this.filters[key]
                if (filter.active) {
                    params.push(key + '=' + encodeURIComponent(filter.value))
                    params.push(key + '.verb=' + encodeURIComponent(filter.verb))
                } else {
                    filter.visible = false
                }
            }

            this.loadAsyncData(params.join('&'))
        },

        clearFilters() {

            // explicitly deactivate all filters
            for (var key in this.filters) {
                this.filters[key].active = false
            }

            // then just "apply" as normal
            this.applyFilters()
        },

        saveDefaults() {

            // apply current filters as normal, but add special directive
            const params = ['save-current-filters-as-defaults=true']
            this.applyFilters(params)
        },

        deleteObject(event) {
            // we let parent component/app deal with this, in whatever way makes sense...
            // TODO: should we ever provide anything besides the URL for this?
            this.$emit('deleteActionClicked', event.target.href)
        },

        checkedRowUUIDs() {
            let uuids = []
            for (let row of this.$data.checkedRows) {
                uuids.push(row.uuid)
            }
            return uuids
        },

        allRowUUIDs() {
            let uuids = []
            for (let row of this.data) {
                uuids.push(row.uuid)
            }
            return uuids
        },
    }
}
