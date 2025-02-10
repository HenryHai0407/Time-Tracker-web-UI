document.addEventListener("DOMContentLoaded", function () {
    // Handle Login Button Click
    document.querySelectorAll(".login-btn").forEach(button => {
        button.addEventListener("click", function () {
            let employeeName = this.dataset.name;
            let location = prompt("Enter your work location (YKH, CC, KPI, ISO, TKK, RED, AOA, JUM):");

            if (location && ["YKH", "CC", "KPI", "ISO", "TKK", "RED", "AOA", "JUM"].includes(location.toUpperCase())) {
                updateTime(employeeName, "Login", location.toUpperCase());
            } else {
                alert("Invalid location. Please enter a valid location.");
            }
        });
    });

    // Handle Logout Button Click
    document.querySelectorAll(".logout-btn").forEach(button => {
        button.addEventListener("click", function () {
            let employeeName = this.dataset.name;
            updateTime(employeeName, "Logout");
        });
    });

    // Function to handle time updates
    function updateTime(name, action, location = null) {
        fetch("/update", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name: name, action: action, location: location })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(action + " time updated successfully!");
                fetchFilteredData(name); // Fetch only the data for the logged-in user
            } else {
                alert("Error updating time: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    }

    // Function to fetch filtered data
    function fetchFilteredData(employeeName) {
        fetch(`/data?name=${encodeURIComponent(employeeName)}`) // Send request with employee name
            .then(response => response.json())
            .then(data => {
                let tableBody = "";
                data.forEach(row => {
                    tableBody += `<tr>
                        <td>${row['Employee Name'] || 'No Name'}</td>
                        <td>${row['Date'] || 'N/A'}</td>
                        <td>${row['Login'] || 'N/A'}</td>
                        <td>${row['Logout'] || 'N/A'}</td>
                        <td>${row['Location'] || 'N/A'}</td>
                        <td>${row['Total working hours'] || 'N/A'}</td>
                    </tr>`;
                });
                document.getElementById("data-body").innerHTML = tableBody;
            })
            .catch(error => console.error("Error fetching data:", error));
    }

    // Filter data when typing in the search input field
    document.getElementById("employee-name").addEventListener("input", function () {
        let selectedName = this.value;
        fetchFilteredData(selectedName); // Filter data based on the name entered
    });

    // Handle Search Button Click
    const searchButton = document.getElementById("search-btn");
    const inputElement = document.getElementById("employee-name");

    // Event listener for the "Search" button
    searchButton.addEventListener("click", function () {
        let selectedName = inputElement.value.trim();
        fetchFilteredData(selectedName); // Fetch filtered data based on the name entered
    });
});
