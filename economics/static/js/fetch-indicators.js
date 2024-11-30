// Get values

function fetchIndicatorValue() {

    // get value
    let indicator = "value";

    $.ajax({
        url: '/economics/get-indicator/'+indicator,
        dataType: 'json',
        success: function(data) {
          console.log(data)
        },
        complete: function () {  
          // finally 
        }
    });
}


function fetchAllValues() {
  fetch('/economics/fetch-all-indicators')
      .then(response => {
          const reader = response.body.getReader();
          const decoder = new TextDecoder("utf-8");

          // Read chunks of the streamed response
          reader.read().then(function process({ done, value }) {
              if (done) {
                  console.log('Stream complete');
                  return;
              }

              const chunk = decoder.decode(value, { stream: true });
              const lines = chunk.trim().split("\n"); // Handle new-line-delimited JSON
              lines.forEach(line => {
                    const data = JSON.parse(line);
                    let classname = "currency-value-" + data.sigla
                    let elements = document.getElementsByClassName(classname);
                  
                    console.log(elements);
                    Array.from(elements).forEach((element) => {
                        element.innerHTML = "";
                        element.innerHTML = data.valor;
                    });
              });

              // Continue reading the stream
              return reader.read().then(process);
          });
      })
      .catch(error => console.error('Error fetching indicators:', error));
}


// Execute on window load
window.onload = fetchAllValues;