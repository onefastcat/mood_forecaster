document.addEventListener('DOMContentLoaded', () => {
        let days = document.getElementsByClassName('date');

        for(let i = 0; i < days.length; i++){

            let today = new Date();
            let date = new Date();
            date.setDate(today.getDate() + i)
            days[i].innerText = date.toDateString().slice(0, 11);
        }
});
