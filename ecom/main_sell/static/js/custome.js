$(document).ready(function () {
    $("#myForm").submit(function (e) {
        e.preventDefault(); // Prevent the default form submission

        // Create a JavaScript object with your data
        var requestData = {
            dataField: $("#").val(),
        };

        // Convert the JavaScript object to JSON
        var jsonData = JSON.stringify(requestData);

        // Make an AJAX POST request
        $.ajax({
            type: "POST",
            url: "/register/", // Replace with your API endpoint URL
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            success: function (response) {
                // Handle the response from the server here
                console.log(response);
            },
            error: function (error) {
                // Handle errors here
                console.error(error);
            },
        });
    });
});
