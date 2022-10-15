

//Get id of radio buttons in upload
let hidden = document.getElementById('hidden');
let show = document.getElementById('show');
let postuser = document.getElementById('postuser');

function usertitle(){
    if(show.checked){
        postuser.innerHTML = '@profile';
        
    }else{
        postuser.innerHTML = 'Anonymous';

    }
}

usertitle()
console.log('hey')