/*
 * Deep Learning Studio - GUI platform for designing Deep Learning AI without programming
 *
 * Copyright (C) 2016-2017 Deep Cognition Labs, Skiva Technologies Inc.
 *
 * All rights reserved.
 */

(function(namespace, $) {
	"use strict";

	var DemoTableDynamic = function() {
		// Create reference to this instance
		var o = this;
		// Initialize app when document is ready
		$(document).ready(function() {
			o.initialize();
		});

	};
	var p = DemoTableDynamic.prototype;

	// =========================================================================
	// INIT
	// =========================================================================

	p.initialize = function() {
		this._initDataTables();
	};

	// =========================================================================
	// DATATABLES
	// =========================================================================

	p._initDataTables = function() {
		if (!$.isFunction($.fn.dataTable)) {
			return;
		}

		// Init the demo DataTables
		this._createUsageDataTable();
	};

    p._createUsageDataTable = function(){
        // create compute table
        $('#compute-usage').DataTable({
            "ajax": '/usage/compute/get/',
            "columns": [
                        { "data": "start" },
                        { "data": "stop" },
                        { "data": "type" },
                        { "data": "hours" },
                        { "data": "cost" },
                    ],
            "footerCallback": function ( row, data, start, end, display ) {
                var api = this.api(), data;   
                // Remove the formatting to get integer data for summation
                var intVal = function ( i ) {
                    return typeof i === 'string' ?
                        i.replace(/[\$,]/g, '')*1 :
                        typeof i === 'number' ?
                            i : 0;
                }; 
                // Total over all pages
                var total = api.column( 4 ).data().
                    reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );   
                // Total over this page
                var pageTotal = api
                    .column( 4, { page: 'current'} )
                    .data()
                    .reduce( function (a, b) {
                        return intVal(a) + intVal(b);
                    }, 0 );    
                // Update footer
                $( api.column( 4 ).footer() ).html(
                    '$'+pageTotal +' ( $'+ total +' total)'
                );
            },
            "columnDefs": [
                {"className": "dt-center", "targets": "_all"}
            ],
			"language": {
				"lengthMenu": '_MENU_ entries per page',
				"search": '<i class="fa fa-search"></i>',
				"paginate": {
					"previous": '<i class="fa fa-angle-left"></i>',
					"next": '<i class="fa fa-angle-right"></i>'
				}
			}
		});

		$('#compute-usage tbody').on('click', 'tr', function() {
			$(this).toggleClass('selected');
		});

        //create disk table
        var table = $('#disk-usage').DataTable({
            "ajax": '/usage/disk/get/',
            "columns": [
                { "data": "type" },
                { "data": "name" },
                { "data": "size" },
                {
                    "targets": -1,
                    "data": null,
                    "defaultContent": '<a href="#" class="delete-usage"><i class="md md-delete"></i></a>'
                }
            ],
            "columnDefs": [
                {"className": "dt-center", "targets": "_all"}
                
            ],
            "footerCallback": function ( row, data, start, end, display ) {
                var api = this.api(), data;
                for (var i=0; i < data.length; i++){
                    if(data[i].type == 'total')
                        $( api.column( 2 ).footer() ).html(data[i].size);
                }     
            },
			"language": {
				"lengthMenu": '_MENU_ entries per page',
				"search": '<i class="fa fa-search"></i>',
				"paginate": {
					"previous": '<i class="fa fa-angle-left"></i>',
					"next": '<i class="fa fa-angle-right"></i>'
				}
			}
		});
        
        $.fn.dataTableExt.afnFiltering.push(function(oSettings, aData, iDataIndex) {
            if (aData[0] == "total")
                return false;
            else 
                return true;
        });

        //delete from row
        $('#disk-usage tbody').on( 'click', '.delete-usage', function () {
            if ( confirm( "Are you sure you want to delete the selected rows?" ) ) {
                var ref = table.row( $(this).parents('tr') );
                var data = ref.data();
                var url;
                var data;
                var csrftoken = getCookie('csrftoken');
                if(data.type == 'project'){
                    url = "/dashboard/delete/";
                    // set project_id below
                    var pid = data.id;
                    console.log(pid);
                    data = {'pid':pid};
                }
                else if(data.type == 'dataset'){
                    url = "/datasets/delete/"
                    var dataset_name = data.name;
                    data = {'dataset_name': dataset_name};
                }
                $.ajax({
                    url: url,
                    type: 'POST',
                    headers: { 'X_METHODOVERRIDE': 'DELETE' ,"X-CSRFToken":csrftoken},
                    contentType: "application/x-www-form-urlencoded",
                    data:data,       
                    success: function(response){
                        if(response.success==0 || response.success == 'OK'){
                            ref.remove().draw();
                        }else{
                            alert(response.message);
                        }
                    }
                }); 
            }
        } );

    }

	// =========================================================================
	namespace.DemoTableDynamic = new DemoTableDynamic;
}(this.materialadmin, jQuery)); // pass in (namespace, jQuery):