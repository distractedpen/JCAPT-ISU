/**********************************
 * Global Variables
 **********************************/
const env = {"SERVICE_HOST": "https://172.19.122.255", "SERVICE_PORT": "8000", "CLIENT_HOST": "0.0.0.0", "CLIENT_PORT": "8001"};
const selectEl = document.getElementById("drill-select");

/********************
 * Fetch data from backend API
 ********************/

function fetchDrillSets() {
    const payload = {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        headers: {
            "Content-Type": 'application/json',
        }
    };
    fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/getDrillSets`, payload)
    .then( (response) => response.json() )
    .then( (json) => {
        const drillSets = json.drill_sets;
        console.log(drillSets);
        drillSets.forEach( (drillset) => {
            console.log(drillset);
            const optionEl = document.createElement("option")
            optionEl.value = drillset['id'];
            optionEl.textContent = drillset['name'];
            selectEl.appendChild(optionEl);
        });
    })
    .catch( (err) => {
        console.log(err);
        return err; 
    });
}

function createDrillSet() {
    localStorage.setItem("isNewDrillSet", true);
    window.location.href = `newDrillSet.html`;
}

function loadToUpdateDrillSet() {
    localStorage.setItem("isNewDrillSet", false);
    localStorage.setItem("drillSetId", selectEl.value);
    window.location.href = `newDrillSet.html`;
}

function deleteDrillSet() {
    if (confirm("This process cannot be undone. Delete this Drill Set?")) {

        const payload = {
            method: "POST",
            mode: "cors",
            cache: "no-cache",
            headers: {
                "Content-Type": 'application/json',
            },
            body: JSON.stringify({
                drillSetId: selectEl.value
            })
        };

        fetch(`${env["SERVICE_HOST"]}:${env["SERVICE_PORT"]}/deleteDrillSet`, payload)
        .then((response) => response.json())
        .then((data) => {
            location.reload();
        })
        .catch((err) => console.log(err));
    }

}


/**********************
 * Setup for page
 **********************/

fetchDrillSets();
