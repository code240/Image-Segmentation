const filter = () => {
    var article = document.getElementById("article").value
    var pos = article.search("<img1>")
    if(pos != -1){
        document.getElementById("img1").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img1" class="file-inp">`;
        document.getElementById("img2").innerHTML = ` `;
        document.getElementById("img3").innerHTML = ` `;

        var pos = article.search("<img2>")
        if(pos != -1){
            document.getElementById("img2").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img2" class="file-inp">`;
            document.getElementById("img3").innerHTML = ` `;
            var pos = article.search("<img3>")
            if(pos != -1){
                document.getElementById("img3").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img3" class="file-inp">`;
            }
        }
    }else{
        document.getElementById("addimg").style.display = "none";
        document.getElementById("noimg").style.display = "block";
        document.getElementById("img1").innerHTML = ` `;
        document.getElementById("img2").innerHTML = ` `;
        document.getElementById("img3").innerHTML = ` `;
    }
} 
const chageimagestatus = () => {
    document.getElementById("addimg").style.display = "block";
    document.getElementById("noimg").style.display = "none";
}



const status_input = () => {
    var status = 0
    if(
        document.getElementById("img1").innerHTML === `<input type="file" accept="image/png, image/jpeg" required="" name="img1" class="file-inp">` ||
        document.getElementById("img1").innerHTML === `<input type="file" accept="image/png, image/jpeg" required name="img1" class="file-inp">`
    ){
        status = 1
        if(
            document.getElementById("img2").innerHTML === `<input type="file" accept="image/png, image/jpeg" required="" name="img2" class="file-inp">` ||
            document.getElementById("img2").innerHTML === `<input type="file" accept="image/png, image/jpeg" required name="img2" class="file-inp">`
        ){
            status = 2
            if(
                document.getElementById("img3").innerHTML === `<input type="file" accept="image/png, image/jpeg" required="" name="img3" class="file-inp">` ||
                document.getElementById("img3").innerHTML === `<input type="file" accept="image/png, image/jpeg" required name="img3" class="file-inp">`
            ){
                status = 3
                
            }
        }
    }
    // console.log("status"+status)
    return status
}

const imgcount = () => {
    var imgcount = 0;
    var article = document.getElementById("article").value
    var pos = article.search("<img1>")
    if(pos != -1){
        imgcount = 1;
        var pos = article.search("<img2>")
        if(pos != -1){
            imgcount = 2;
            var pos = article.search("<img3>")
            if(pos != -1){
                imgcount = 3;
            }
        }
    }
    // console.log(imgcount)
    return imgcount
}
const removeExtraimage = (x) => {
    changement = 0;
    inputcount = status_input()
    // alert("input count:"+inputcount +"...imageCount:"+x)
    if(inputcount != x){
        if(x==0){
            document.getElementById("img1").innerHTML = ` `;
            document.getElementById("img2").innerHTML = ` `;
            document.getElementById("img3").innerHTML = ` `;
            changement = 3;
        }
        if(x == 1){
            document.getElementById("img1").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img1" class="file-inp">`;
            document.getElementById("img2").innerHTML = ` `;
            document.getElementById("img3").innerHTML = ` `;
            changement = 2;
        }
        if(x == 2){
            document.getElementById("img1").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img1" class="file-inp">`;
            document.getElementById("img2").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img2" class="file-inp">`;
            document.getElementById("img3").innerHTML = ` `;
            changement = 1;
        }
        if(x == 3){
            document.getElementById("img1").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img1" class="file-inp">`;
            document.getElementById("img2").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img2" class="file-inp">`;
            document.getElementById("img3").innerHTML = `<input type="file" accept="image/png, image/jpeg" required name="img3" class="file-inp">`;
            changement = 4;
        }
    }
    return changement
}

const Save_article = () => {
    const img = imgcount();
    console.log(img)
    changes = removeExtraimage(img)
    if(changes != 0) {
        alert("Check Your Images, There is some changes ")
        return false
    }else{
        return true
    }
}


// function getImageCount(content){
//     article = content
//     var pos = article.search("<img1>")
//     imgcount = 0
//     if(pos != -1){
//         imgcount = 1;
//         var pos = article.search("<img2>")
//         if(pos != -1){
//             imgcount = 2;
//             var pos = article.search("<img3>")
//             if(pos != -1){
//                 imgcount = 3;
//             }
//         }
//     }
//     return imgcount
// }