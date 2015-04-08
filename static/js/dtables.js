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

$.fn.asmetDataTable = function(ajaxUrl, columns, order, server_params) {
  // TODO: how to properly pass this up?
    asmetDataTable  = this.dataTable({
//    responsive: {
//          details: {
//            type: 'inline',
//            renderer: function ( api, rowIdx ) {
 //             var theRow = api.row(rowIdx);
  //            console.log("row: ", theRow.data());
//              //console.log("cache: ", theRow.cache('search'));
//                    // Select hidden columns for the given row
//                    var data = api.cells( rowIdx, ':hidden' ).eq(0).map( function ( cell ) {
//                        var header = $( api.column( cell.column ).header() );
//     
//                        return '<tr>'+ '<td>'+ header.text()+'</td>' + '<td>&nbsp;</td>' + '<td>'+  $( api.cell( cell ).node() ).html() + '</td>'+ '</tr>';
//                    } ).toArray().join('');
//     
//                    return data ?
//                        $('<table/>').append( data ) :
//                        false;
 //               }
 //         }
 //   },
    bFilter: false,
    processing: true,
    serverSide: true,
    sAjaxSource: ajaxUrl,
    columns: columns,
    order: order || [0, 'asc'],
    fnServerParams:  function ( aoData ) {
        aoData.push({ "name": "sParams", "value": server_params});
    },
    /* TODO: come back and work out how to highlight odd rows
    "fnRowCallback": function (nRow, aData, iDisplayIndex, iDisplayIndexFull) {
        if (aData.selectable) {
            console.log("row" + nRow.id + "selectable");
            $(nRow).css('background-color', 'grey').css('cursor', 'pointer');
            $(nRow).addClass('dt-hover');
      }
    }, */


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
}
