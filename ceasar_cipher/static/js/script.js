google.charts.load('current', {'packages':['bar']});
google.charts.setOnLoadCallback(draw_chart);

$("#button_encode").click(function () {
    let send_data = {};
    send_data.plaintext = $('#input_textarea').val();
    send_data.key = $('#input_key').val();
    send_data.action = "encode";
    if (validate_textarea() == true && validate_key() == true){
        send_to_server(send_data);
        document.getElementById('info_block').style.display = 'block';
    }

});

$("#button_decode").click(function () {
    let send_data = {};
    send_data.plaintext = $('#input_textarea').val();
    send_data.key = $('#input_key').val();
    send_data.action = "decode";

    if (validate_textarea() == true && validate_key() == true){
        send_to_server(send_data);
        document.getElementById('info_block').style.display = 'block';
    }
});

function send_to_server(send_data) {
    let csrf_token = $('#encode_decode_form [name="csrfmiddlewaretoken"]').val();
    console.log(send_data);
    $.ajax({
        headers: { "X-CSRFToken": csrf_token },
        url: "",
        type: 'POST',
        dataType: "json",
        data: send_data,
        success: function (data) {
            $('#output_textarea').html(data['text']);
            console.log('ajax OK');
            draw_chart(data);

        },
        error: function () {
            console.log('ajax ERROR')
        },
    });
}

$("#input_textarea").on('input',function(e){
    let  send_data = {};
    document.getElementById('info_block').style.display = 'block';
    if(e.target.value === ''){
        // Textarea has no value
    } else {
        send_data.plaintext = $('#input_textarea').val();
        console.log(send_data.plaintext);
        send_data.action = 'f_a';
        send_to_server(send_data);
    }
});

function validate_key() {
    let key = $('#input_key').val();
    if(key > 0 && key <= 26){
        $('#input_key').removeClass('empty_field');
        return true
    }else {
        console.log('key must be 1 - 26');
        $('#input_key').addClass('empty_field');
    }
}

function validate_textarea() {
    if ($('#input_textarea').val() == ''){
        $('#input_textarea').addClass('empty_field');
        console.log("text is required");
        return false;
    }else {
        $('#input_textarea').removeClass('empty_field');
        return true;
    }
}

function draw_chart(data) {

    let chart_data = new google.visualization.DataTable();
    chart_data.addColumn('string','Letter');
    chart_data.addColumn('number','Frequency');

    for (let i = 0; i <= 25; i++){
        chart_data.addRows([
            [data.frequency_analysis.analysis[i].letter, data.frequency_analysis.analysis[i].frequency],
        ]);

    }

    let options = {
        width: 850,
        height: 100,
        bar: { groupWidth: "90%" },
        backgroundColor: '#F5F5F5',
    };

    let chart = new google.charts.Bar(document.getElementById('info_block'));
    chart.draw(chart_data, google.charts.Bar.convertOptions(options));
}

