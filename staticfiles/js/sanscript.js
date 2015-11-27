// =============================================================================
// get url parameters

function getUrlParameter(sParam)
{
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++)
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam)
        {
            value = decodeURIComponent(sParameterName[1])
            value = value.replace(/\+/g, ' ')
            return value;
        }
    }
}

// =============================================================================
// export table to csv

function exportTableToCSV($table, filename) {
    // var $rows = $table.find('tr:has(td)'),
    var $rows = $table.find('tr'),
        // Temporary delimiter characters unlikely to be typed by keyboard
        // This is to avoid accidentally splitting the actual contents
        tmpColDelim = String.fromCharCode(11), // vertical tab character
        tmpRowDelim = String.fromCharCode(0), // null character
        // actual delimiter characters for CSV format
        colDelim = '";"',
        rowDelim = '"\r\n"',
        // Grab text from table into CSV formatted string
        csv = '"' + $rows.map(function (i, row) {
            var $row = $(row),
                $cols = $row.find('th, td');
            return $cols.map(function (j, col) {
                var $col = $(col), text;
                $col.find("br").replaceWith("<div>{{BR_MARKER}}</div>"); // <br> to line_break
                text = $col.text().replace(/{{BR_MARKER}}/g, "\r\n");    // <br> to line_break
                text = text.trim()
                text = text.replace('"', '""'); // escape double quotes
                if (isNaN(text) == false) {
                    text = text.replace('.', ',');
                };
                return text
            }).get().join(tmpColDelim);
        }).get().join(tmpRowDelim)
            .split(tmpRowDelim).join(rowDelim)
            .split(tmpColDelim).join(colDelim) + '"',
        // Data URI
        csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csv);
    $(this)
        .attr({
        'download': filename,
            'href': csvData,
            'target': '_blank'
    });
}

// =============================================================================
// fix first row in top position

function scrollWrappers(wrapper1, wrapper2) {
    wrapper1.scroll(function(){
        wrapper2.scrollLeft(wrapper1.scrollLeft());
    });
    wrapper2.scroll(function(){
        wrapper1.scrollLeft(wrapper2.scrollLeft());
    });
};

function resizeFirstWrapper(wrapper1, wrapper2) {
    wrapper1.width(wrapper2.width());
    wrapper1.find('table').width(wrapper2.find('table').width());
};

function fixTableSizes(wrapper2) {
    wrapper2.find('tr:first td').each(function() {
        $(this).css('width', $(this).outerWidth())
    });
    wrapper2.find('tr:nth-child(2) td').each(function() {
        $(this).css('width', $(this).outerWidth());
    });
    wrapper2.find('table').css('width', wrapper2.find('table').width());
};

function fixDiv(wrapper1, wrapper2, xtimes) {
    var $cache = $('.wrapper1');
    if ($(window).scrollTop() > 180){
        xtimes.detach().appendTo(wrapper1.find('table'));
        $cache.css({
            'position': 'fixed',
            'top': '0',
        });
        wrapper1.find('table th').hide();
    }
    else {
        if ($cache.css('position') == 'fixed') {
            wrapper1.find('table th').show();
            xtimes.detach().prependTo(wrapper2.find('table'));
            $cache.css({
                'position': 'relative',
                'top': 'auto',
            });
        }
    }
};

// =============================================================================

