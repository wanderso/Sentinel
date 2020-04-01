require.undef('sentinel_table');

define('sentinel_table', ["@jupyter-widgets/base"], function(widgets) {

    var SentinelTable = widgets.DOMWidgetView.extend({

        // Render the view.
        render: function()
        {
            this.table_output = document.createElement('TABLE');
            this.table_output.disabled = this.model.get('disabled');

            this.entry_data = this.model.get('entry_list');
            this.description_data = this.model.get('entry_descriptions');
            this.class_type = this.model.get('class_list');
            this.table_header = this.model.get('table_header');

            this.selected_entry = null;

            this.toggle_class_list(this.table_output);
            this.update_list();

            this.el.appendChild(this.table_output);

            // Python -> JavaScript update
            this.model.on('change:entry_list', this.entries_changed, this);
            this.model.on('change:description_data', this.entries_changed, this);
            this.model.on('change:disabled', this.disabled_changed, this);
            this.model.on('change:reset_flag', this.clear_selection, this);

            // JavaScript -> Python update
            this.table_output.onchange = this.input_changed.bind(this);
        },

        toggle_class_list: function(elem)
        {
            for (var j = 0; j < this.class_type.length; j++)
            {
                elem.classList.toggle(this.class_type[j]);
            }
        },

        toggle_selection: function(elem)
        {
            elem.classList.toggle("desc-selected");
            elem.firstChild.childNodes[1].classList.toggle("hide-display")
        },

        clear_selection: function()
        {
            //alert("Clearing selection");
            if (this.selected_entry !== null)
            {
                this.toggle_selection(this.selected_entry);
            }
            this.model.set('selected_value_index', -1);
            this.model.save_changes();
            this.selected_entry = null;
        },

        select_entry: function(elem, index)
        {
            //alert("Selecting different entry");
            if (this.selected_entry !== null)
            {
                this.toggle_selection(this.selected_entry);
            }
            if (this.selected_entry == elem)
            {
                this.model.set('selected_value_index', -1);
                this.model.save_changes();
                this.selected_entry = null;
                return false;
            }
            this.toggle_selection(elem);
            this.selected_entry = elem;
            this.model.set('selected_value_index', index);
            this.model.save_changes();
            return false;
        },


        update_list: function()
        {
          let st = this;
          var tr = document.createElement('tr');
          var th = document.createElement('th');
          var tn = document.createTextNode(this.table_header);

          this.toggle_class_list(tr)
          this.toggle_class_list(th)

          tr.appendChild(th);
          th.appendChild(tn);

          this.table_output.appendChild(tr)

        /*     trait_name = str(value)
               trait_desc = value.get_description()
               table_text += "<tr class='environment-table'><td class='environment-table{4}', "\
               "oncontextmenu='return selectRow(this)', id='{2}'>{0}<div "\
               "class='environment-table-description{3}' >{1}</div></td></tr>\n".format(
               trait_name, trait_desc, str(hash(trait_name)) + "_environment_trait", hidden_val, select_env) */

          for (let i = 0; i < this.entry_data.length; i++)
          {
                var index = i;
                tr = document.createElement('tr');
                var td = document.createElement('td');
                var tiv = document.createElement('div');

                this.toggle_class_list(td)
                this.toggle_class_list(tr)
                this.toggle_class_list(tiv)

                tr.appendChild( td );
                td.appendChild( document.createTextNode(this.entry_data[i]) );
                td.appendChild( tiv );
                tiv.appendChild( document.createTextNode(this.description_data[i]) );
                tiv.classList.toggle("environment-table-description")
                tiv.classList.toggle("hide-display")

                tr.oncontextmenu = function() { return st.select_entry(this, i); };

                this.table_output.appendChild(tr);
            }
        },

        entries_changed: function()
        {
            while (this.table_output.firstChild)
            {
                this.table_output.firstChild.remove();
            }
            this.entry_data = this.model.get('entry_list');
            this.update_list()
        },

        disabled_changed: function()
        {
            this.table_output.disabled = this.model.get('disabled');
        },

        input_changed: function()
        {
            this.model.set('value', this.table_output.value);
            this.model.save_changes();
        },

        selection_changed: function()
        {
            let ind = this.model.get('selected_value_index')
            alert(ind);
            /* Okay, that failed exactly the way I thought it would. Figure this out in the morning */
        },

    });

    return {
        SentinelTable: SentinelTable
    };
});