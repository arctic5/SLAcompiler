function update(){
    if(document.getElementById("download").getBoundingClientRect().top < window.innerHeight/2){
        document.querySelector(".nav").getElementsByTagName("li")[0].className = "";
        document.querySelector(".nav").getElementsByTagName("li")[1].className = "";
        document.querySelector(".nav").getElementsByTagName("li")[2].className = "active";
    }
    else if(document.getElementById("about").getBoundingClientRect().top < window.innerHeight/2){
        document.querySelector(".nav").getElementsByTagName("li")[0].className = "";
        document.querySelector(".nav").getElementsByTagName("li")[1].className = "active";
        document.querySelector(".nav").getElementsByTagName("li")[2].className = "";
    }
    else{
        document.querySelector(".nav").getElementsByTagName("li")[0].className = "active";
        document.querySelector(".nav").getElementsByTagName("li")[1].className = "";
        document.querySelector(".nav").getElementsByTagName("li")[2].className = "";
    }
    requestAnimationFrame(update);
}

requestAnimationFrame(update);