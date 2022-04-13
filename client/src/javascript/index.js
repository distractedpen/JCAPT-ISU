/**********************************
 * Global Variables
 **********************************/
const env = {"SERVICE_HOST": "https://172.19.124.246", "SERVICE_PORT": "8000", "CLIENT_HOST": "0.0.0.0"};
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
            "Origin": `${env["CLIENT_HOST"]}`
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

function getDrill(){
    localStorage.setItem("drill_set", selectEl.value);
}


/**********************
 * Setup for page
 **********************/

 fetchDrillSets();