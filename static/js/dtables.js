function get_id(me) {
    var id_row = me.closest('tr').attr('id');
    if (!id_row) {
        id_row = me.closest('table').closest('tr').prev().attr('id');
    }
    if (!id_row) {
        console.log("id row missing");
        return none;
    } else {
        return id_row;
    }
}

$.fn.asmetDataTable = function(ajaxUrl, columns, options) {
    options = options || {};
    asmetDataTable  = this.dataTable({
    sScrollX: true,
    bFilter: false,
    processing: true,
    serverSide: true,
    sAjaxSource: ajaxUrl,
    columns: columns,
    displayLength: 30,
    order: options.order || [0, 'asc'],
    fnServerParams:  function ( aoData ) {
        if ('filter' in options) {
            aoData.push({ "name": "sParams", "value": options.filter});
        }
    },
    fnRowCallback: function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
        if ('row_callback' in options) {
            options.row_callback(nRow, aData);
        }
    }, 


    fnServerData: function (url, aoData, callback, settings) {
        var sSearch = null;
        var iSortCol = null;
        var iSortDir = null;
        var sParams = null;
        for (var ii = 0; ii < aoData.length; ii++) {
            switch (aoData[ii].name) {
            case 'sSearch':
                sSearch = aoData[ii].value;
                break;
            case 'iSortCol_0':
                iSortCol = aoData[ii].value;
                break;
            case 'sSortDir_0':
                iSortDir = aoData[ii].value;
                break;
            case 'sParams':
                sParams = aoData[ii].value;
                break;
            }
            // console.log(aoData[i].name + " " + aoData[i].value);
        }
        data = [];
        data.push({name: "length", value: settings._iDisplayLength });
        data.push({name: "start", value: settings._iDisplayStart });
        data.push({name: "draw", value: settings.iDraw });
        if (sSearch) {
            data.push({name: "search", value: sSearch });
        }
        if (iSortCol) {
            data.push({name: "sortCol", value: iSortCol });
        }
        if (iSortDir) {
            data.push({name: "sortDir", value: iSortDir });
        }
        if (sParams) {
            data.push({name: "sParams", value: sParams});
        }

        settings.jqXHR = $.ajax({
            url: url,
            data: data,
            success: function (json) {
                $(settings.oInstance).trigger('xhr', settings);
                callback(json);
            },
            dataType: "json",
            cache: false,
            error: function (xhr, error, thrown) {
                if (error == "parsererror") {
                    alert("DataTables warning: JSON data from server could not be parsed. " +
                                        "This is caused by a JSON formatting error.");
                }
            }
        });
      }
    });
    $('#searchbox').keypress(function (e) {
          if (e.which == 13) {
              console.log($("#searchbox").value);
               asmetDataTable.fnFilter($("#searchbox").val());
          }
    });
    $("#dosearch").click(function() {
           asmetDataTable.fnFilter($("#searchbox").val());
    });
    $("#clear-search").click(function() {
           $("#searchbox").val('');
           asmetDataTable.fnFilter('');
    });
    if ('fixed_columns' in options) {
         new $.fn.dataTable.FixedColumns(asmetDataTable, {
            leftColumns: options.fixed_columns
        });
    }
    return asmetDataTable;
}
