var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['{% m for m in months %}'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255,99,123)',
            borderColor: 'rgb(255,99,132)',
            data: [0, 10, 5, 2, 20, 30, 45],
        }]
    },
    options: {}
});
let mylabel = '{{ months }}';
alert('{{months[2]}}');
console.log(mylabel)