
const NumericInput = {
    template: [
        '<b-input',
        ':name="name"',
        ':value="value"',
        '@keydown.native="keyDown"',
        '@input="valueChanged"',
        '>',
        '</b-input>'
    ].join(' '),

    props: {
        name: String,
        value: String,
        allowEnter: Boolean
    },

    methods: {

        keyDown(event) {
            // by default we only allow numeric keys, and general navigation
            // keys, but we might also allow Enter key
            if (!key_modifies(event) && !key_allowed(event)) {
                if (!this.allowEnter || event.which != 13) {
                    event.preventDefault()
                }
            }
        },

        valueChanged(value) {
            this.$emit('input', value)
        }

    }
}

Vue.component('numeric-input', NumericInput)
