$(document).ready(
    function init_datatables(){
        if(typeof($.fn.datatable) === 'undifined'){
            return ;
        }
    $('#datatable_hacker_news').DataTable();
});