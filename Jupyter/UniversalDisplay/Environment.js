function classChange(elem, className)
{
    elem.classList.toggle(className);
}

function selectRow(elem)
{
    var table = elem.parentElement.parentElement

    var selec_old = table.querySelector(".desc-selected")
    if (selec_old !== null && selec_old !== elem)
    {
        var selec_desc_env = selec_old.querySelector(".environment-table-description")
        classChange(selec_desc_env, "hide-display")
        classChange(selec_old, "desc-selected")
    }
    var desc_env = elem.querySelector(".environment-table-description")

    classChange(desc_env, "hide-display")
    classChange(elem, "desc-selected")

    var kernel = IPython.notebook.kernel;
    kernel.execute("omega.receive_message(\"environment select " + elem.id + "\");")

    return false;
}

window.selectRow = selectRow;
