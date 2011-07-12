import Qt 4.7
import net.khertan.qmlcomponents 1.0

Rectangle {
    id:view
    color: "grey"
    width:800
    height:480

    property string filepath
    property string filename

    Flickable {
        id:flicker
        width: parent.width; height: parent.height - 64
        contentWidth: editor.width; contentHeight: editor.height + 48     
        clip: true
        //overshoot:false

        Rectangle {
            id:titlebar
            width:parent.width
            height:48
            anchors.top: parent.top
            color:'black'
            Text {
                id:titlelabel
                anchors.fill: parent
                anchors.leftMargin: 5
                font { bold: true; family: "Helvetica"; pixelSize: 18 }
                color:'white'
                text:((editor.modification==true) ? '* ':'')+view.filepath
                verticalAlignment: "AlignVCenter"
            }        
        }
        
        QmlTextEditor {
            id:editor
            filepath: view.filepath
            anchors.top: titlebar.bottom
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            onWidthChanged:{
                flicker.contentWidth=editor.width
            }
            onHeightChanged:{
                flicker.contentHeight=editor.height+48
            }
        }
    }
        
    ScrollBar{
        id:texteditscroller
        scrollArea: flicker
        width: 10
        anchors.right: parent.right
        height: parent.height
    }

    MessageBox{
        id:message
        opacity: 0
    }

    ToolBar{
        id:toolbar
        height:64
        width: parent.width
        anchors.bottom: parent.bottom
        onIndentButtonClicked:{
            editor.indent()
        }
        onUnIndentButtonClicked:{
            editor.unindent()
        }
        onCommentButtonClicked:{
            editor.comment()
        }
        onButton6Clicked:
        {
            message.text='This feature is not yet implemented';
            message.opacity=1
        }
        onButton7Clicked:
        {
            message.text='This feature is not yet implemented';
            message.opacity=1
        }
        onButton8Clicked:
        {
            message.text='This feature is not yet implemented';
            message.opacity=1
        }
        onSaveButtonClicked:
        {
            editor.save()
        }
    }

}