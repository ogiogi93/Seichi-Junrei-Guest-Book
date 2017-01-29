/**
 * Created by Ogiwara on 2017/01/29.
 */
(function () {
    var takePicture = document.querySelector("#take-picture"),
        showPicture = document.querySelector("#show-picture");

    if (takePicture && showPicture) {
        // イベントを設定
        takePicture.onchange = function (event) {
            // 撮影された写真または選択された画像への参照を取得
            var files = event.target.files,
                file;
            if (files && files.length > 0) {
                file = files[0];
                try {
                    // window.URL オブジェクトを取得
                    var URL = window.URL || window.webkitURL;

                    // ObjectURL を作成
                    var imgURL = URL.createObjectURL(file);

                    // ObjectURL を img の src に設定
                    showPicture.src = imgURL;

                    // ObjectURL を破棄
                    URL.revokeObjectURL(imgURL);
                }
                catch (e) {
                    try {
                        // createObjectURL がサポートされていない場合にフォールバック
                        var fileReader = new FileReader();
                        fileReader.onload = function (event) {
                            showPicture.src = event.target.result;
                        };
                        fileReader.readAsDataURL(file);
                    }
                    catch (e) {
                        //
                        var error = document.querySelector("#error");
                        if (error) {
                            error.innerHTML = "Neither createObjectURL or FileReader are supported";
                        }
                    }
                }
            }
        };
    }
})();
