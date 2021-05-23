//Search by calling AJAX and hide any previous results
function runSearch(search_term) {
        $('#results').hide();
        $('#tbody').empty();
        $('#database').empty();

        //Transform all the form parameters into a string
        var frmStr = $('#gene_search').serialize();

        $.ajax({
                url: './pgQuery.cgi',
                dataType: 'json',
                data: frmStr,
                success: function(data, textStatus, jqXHR) {
                        processJSON(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                        alert('Failed! textStatus: (' + textStatus +
                                ') and errorThrown: (' + errorThrown + ')');
                }
        });
}

// Process JSON object from cgi file and set the span that lists the match count
function processJSON(data) {
        $('#match_count').text(data.match_count);

        //Keep track of row identifiers
        var next_row_num = 1;

        //Iterate over each match and add a row to the result table for each
        $.each(data.matches, function(i, data) {

                //Add the columns
                $('<td/>', {"db_element": data.unique_name}).appendTo('#database');
                $('<td/>', {"db_element": data.url}).appendTo('#database');
                $('<td/>', {"db_element": data.accession}).appendTo('#database');
                $('<td/>', {"db_element": data.version}).appendTo('#database');
        });

        //now show the result section that was previously hidden
        $('#results').show();
}

// Collapsible protein boxes
var collapsible_count = 1;

// Clear the container for multiple matches
$('#container').empty();

// Create a new collapsible box for each protein match
$.each(data.matches, function(i, data) {

        var accordion = '<div class="panel-group" id="accordion"><div class="panel panel-default"><div class="panel-heading"><h4 id="panel-title" class="panel-title"><a id ="collapse_title" data-toggle="collapse" data-parent="#accordion" href="#collapse' + collapse_count + '">' + val.value + '</a></h4></div><div id="collapse' + collapse_count + '" class="panel-collapse collapse"><div id="panel_body' + collapse_count + '" class="panel-body"></div></div>';

        $(accordion).appendTo('#container')

        // Add additional data to table
        var output = '<table id=output' + collapse_count + '>';

        output += '<tr><td>Trait:</td><td id="qualities">' + data.trait + '</td></tr>';
        output += '<tr><td>SNP rs:</td><td id="qualities">' + data.snp_rs + '</td></tr>';
        output += '<tr><td>Context:</td><td id="qualities">' + data.context + '</td></tr>';
        output += '<tr><td>Gene:</td><td id="qualities">' + data.gene + '</td></tr>';
        output += '<tr><td>Gene id:</td><td id="qualities">' + data.gene_id + '</td></tr>';
        output += '<tr><td>Gene 2:</td><td id="qualities">' + data.gene_2 + '</td></tr>';
        output += '<tr><td>Gene id 2:</td><td id="qualities">' + data.gene_id_2 + '</td></tr>';
        output += '<tr><td>P-value:</td><td id="qualities">' + data.p_value + '</td></tr>';
        output += '<tr><td>Source:</td><td id="qualities">' + data.source + '</td></tr>';
        output += '<tr><td>Pubmed:</td><td id="qualities">' + data.pubmed + '</td></tr>';
        output += '<tr><td>Analysis id:</td><td id="qualities">' + data.analysis_id + '</td></tr>';
        output += '<tr><td>Study id:</td><td id="qualities">' + data.study_id + '</td></tr>';
        output += '<tr><td>Study name:</td><td id="qualities">' + data.study_name + '</td></tr>';

        output += '</table>';
        $(output).appendTo('#panel_body' + collapse_count);

        collapse_count++;


});

// Run javascript once the page is ready
$(document).ready(function() {
        $('#submit').click(function() {
                runSearch();
                return false;
        });
        autocomplete();
});


        //Position the search box at the top of the screen
        $('#gene_search').css({'position': 'absolute', 'top': '1%', 'left': '40%', 'font-size': '18px'});

        //Show hidden items
        $('#results').show();
        $('#databases').show();

        // Autocomplete user input
        function autocomplete() {
                $('#search_term').autocomplete({
                        source:function(request, response){
                                $.ajax({
                                        url: './gQuery.cgi',
                                        dataType: 'json',
                                        data: {
                                                search_term: request.term
                                        },
                                        success: function(data, textStatus, jqXHR) {
                                                if(!data.matches.length){
                                                        var result = [
                                                        {
                                                        label: 'No proteins found',
                                                        value: response.term
                                                }];
                                                response(result);
                                        }

                                                else {
                                                        response($.map(data.matches, function(results){
                                                                return {
                                                                        label: results.value
                                                                }
                                                        }));
                                                }
                                        }
                                });
                        }


                });
}
