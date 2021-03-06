// When comparing groups' names we do not know what was initial sort order (and we would like to keep it fixed)
// Furthermore, we also do not know which table's (if there are multiple tables on the page) groups we are at
// So we make a list of all groups from all tables joined together and use this to compare groups' names
// There should be no be equally named groups in different tables
var allGroups = [];

function testIP(data) {
	return /^(\d{1,3}\.){3}\d{1,3}(\/\d{1,2})?$/.test(data);
}

function extractFirstElementText(data) {
	return $(data).eq(0).text();
}

function cleanDate(data) {
	if (/^\s*never\s*/.test(data)) {
		return "01 Jan 1970 00:00:00";
	}
	return data.replace(/\//g, " ").replace(/,/g, "");
}

jQuery.fn.dataTableExt.aTypes.push(
	function (sData) {
		if (testIP(sData)) {
			return 'ip-address';
		}
		return null;
	},
	function (sData) {
		// We use valid HTML data where this characters should be escaped in text so we can find tags this way
		if (/[<>]/.test(sData)) {
			if (testIP(extractFirstElementText(sData))) {
				return 'html-ip-address';
			}
			else if (/^\s*$/.test(sData.replace(/<.*?>/g, ""))) {
				// Nothing except HTML tags are in data, we will try to use alt attribute
				return 'html-alt';
			}
			else {
				// Will use text between HTML tags
				return 'html';
			}
		}
		return null;
	},
	function (sData) {
		// This code is duplicated in reverse in conversion.py file. Keep them in sync.
		if (/^\d+(\.\d+)?\s+(KB|MB|GB)$/.test(sData)) {
			return 'byte-size';
		}
		return null;
	},
	function (sData) {
		var parse = Date.parse(cleanDate(sData));
		if (!isNaN(parse)) {
			return 'date-clean';
		}
		return null;
	}
);

function compare(a, b) {
	return ((a < b) ? -1 : ((a > b) ? 1 : 0));
}

function getAlt(el) {
	var el = $(el);
	var alt = el.attr('alt') || el.find('[alt]').attr('alt') || "";
	return alt.toLowerCase();
}

jQuery.fn.dataTableExt.oSort['html-alt-asc'] = function (a, b) {
	return compare(getAlt(a), getAlt(b));
};

jQuery.fn.dataTableExt.oSort['html-alt-desc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['html-alt-asc'](b, a);
};

// This code is duplicated in reverse in conversion.py file. Keep them in sync.
function toKbytes(n) {
	var v = parseFloat(n);
	if (/MB/.test(n)) {
		v *= 1024.0;
	}
	else if (/GB/.test(n)) {
		v *= 1048576.0;
	}
	return v;
}

jQuery.fn.dataTableExt.oSort['byte-size-asc'] = function (a, b) {
	return compare(toKbytes(a), toKbytes(b));
};

jQuery.fn.dataTableExt.oSort['byte-size-desc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['byte-size-asc'](b, a);
};

jQuery.fn.dataTableExt.oSort['ip-address-asc'] = function (a, b) {
	var as = a.split(/[./]/);
	var bs = b.split(/[./]/);
	for (var i = 0; i < as.length; i++) {
		if (i >= bs.length) {
			return 1;
		}
		var comp = as[i] - bs[i];
		if (comp != 0) {
			return comp;
		}
	}
	if (i < bs.length) {
		return -1;
	}
	return 0;
};

jQuery.fn.dataTableExt.oSort['ip-address-desc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['ip-address-asc'](b, a);
};

jQuery.fn.dataTableExt.oSort['html-ip-address-asc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['ip-address-asc'](extractFirstElementText(a), extractFirstElementText(b));
}

jQuery.fn.dataTableExt.oSort['html-ip-address-desc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['html-ip-address-asc'](b, a);
};

jQuery.fn.dataTableExt.oSort['group-sort-asc'] = function (a, b) {
	return compare($.inArray(a, allGroups), $.inArray(b, allGroups));
};

jQuery.fn.dataTableExt.oSort['group-sort-desc'] = function (a, b) {
	return jQuery.fn.dataTableExt.oSort['group-sort-asc'](b, a);
};

function dateCompare(a, b) {
	var x = Date.parse(cleanDate(a));
	var y = Date.parse(cleanDate(b));

	if (isNaN(x)) {
		x = 0;
	}
	if (isNaN(y)) {
		y = 0;
	}

	return x - y;
}

jQuery.fn.dataTableExt.oSort['date-clean-asc'] = function (a, b) {
	return dateCompare(a, b);
};

jQuery.fn.dataTableExt.oSort['date-clean-desc'] = function (a, b) {
	return dateCompare(b, a);
};

function groupDrawCallback(table) {
	return function (oSettings) {
		if (oSettings.aiDisplay.length == 0) {
			return;
		}
		
		var trs = $(table).find('tbody tr');
		var colspan = trs.eq(0).find('td').length;
		var lastGroup = "";
		trs.each(function (i) {
			var displayIndex = oSettings._iDisplayStart + i;
			var group = oSettings.aoData[oSettings.aiDisplay[displayIndex]]._aData[0];
			if (group != lastGroup) {
				$("<tr />").addClass("section_title").append(
					$("<td />").attr("colspan", colspan).html(group)
				).insertBefore($(this));
				lastGroup = group;
			}
		});
	};
}

$(document).ready(function() {
	if (typeof tablesConfig == "undefined") {
		tablesConfig = [];
	}
	$('table.listing:has(thead)').each(function (t) {
		var sections = [];
		var config = $.extend({
			"entryName": "entries",
			"sortColumn": []
		}, tablesConfig[t]);
		var entryName = config.entryName;
		var sortColumn = config.sortColumn;
		
		$(this).find('tbody tr').each(function (i) {
			if ($(this).is('.section_title')) {
				var content = $(this).find('td').html();
				sections.push(content);
				allGroups.push(content);
				$(this).remove();
			}
			else if (sections.length != 0) {
				$(this).prepend($("<td />").html(sections[sections.length - 1]));
			}
		});
		if (sections.length != 0) {
			$(this).find('thead tr').prepend($("<th />"));
		}
		
		var columns = [];
		$(this).find('thead th').each(function (i) {
			if ((i == 0) && (sections.length != 0)) {
				columns.push({
					"bVisible": false,
					"bSearchable": true,
					"bSortable": true,
					"sType": 'group-sort'
				});
			}
			else if (/^\s*$/.test($(this).text())) {
				// We ignore columns with empty header
				columns.push({
					"bVisible": true,
					"bSearchable": false,
					"bSortable": false
				});
			}
			else {
				columns.push({});
			}
		});
	
		$.each(sortColumn, function (i, val) {
			if (sections.length != 0) {
				val[0]++;
			}
			if (val[1] == "desc") {
				columns[val[0]].asSorting = ["desc", "asc"];
			}
		});
	
		if (($(this).find('tbody td:not([colspan])').length > 0) || ($('table.listing').find('tbody td[colspan=1]').length > 0)) {
			$(this).dataTable({
				"bPaginate": false,
				"bLengthChange": true,
				"bFilter": true,
				"bSort": true,
				"oSearch": {
					"sSearch": "",
					"bEscapeRegex": false
				},
				"bInfo": true,
				"bAutoWidth": false,
				"bProcessing": false,
				"bSortClasses": false,
				"bStateSave": false,
				"bServerSide": false,
				"aoColumns": columns,
				"aaSortingFixed": (sections.length != 0 ? [[ 0, 'asc' ]] : null),
				"aaSorting": sortColumn,
				"fnDrawCallback": (sections.length != 0 ? groupDrawCallback(this) : null),
				"sDom": 'ift<"clear">',
				"oLanguage": {
					"sZeroRecords": "No matching " + entryName + " found",
					"sInfo": "_TOTAL_ " + entryName + " shown",
					"sInfoEmpty": "0 " + entryName + " shown",
					"sInfoFiltered": "(from _MAX_ all " + entryName + ")",
					"sInfoPostFix": "",
					"sSearch": "Filter:"
				}
			});
		}
	});
});
