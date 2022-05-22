# python-bayer-edit
EDIT BAYERED FILES (PNG/FITS/TIFF/RAW)

天文関係のみなさまこんばんは…
このPythonスクリプトは
「SharpCapで保存」した
「PNG形式のスナップショット」との
相互変換をするものです。

・PNG08Debayer / PNG08Rebayer
＊8bit-grayの画像をTRUE COLORに
RGGBでデモザイク/その逆変換

・PNG16Debayer / PNG16tiff
＊16bit-gray用 / tiff形式にも変換

※以上には追加ライブラリが必要になります。
pillow / imageio / opencv-python

・PNG-Debayer
＊ライブラリを使わずに書いたフルスクラッチ版
PNG 8bit-gray / 16bit-gray 両対応！

・Fits-Decorder / Fits-Debayer
＊fitsファイル処理用(テスト中) PNGに変換します。

・raw2tiff
＊raw 画像を読み込み tiff(48bit)とpng(bayerd)に変換します。



