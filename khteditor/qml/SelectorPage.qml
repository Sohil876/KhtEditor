import QtQuick 1.1
import com.nokia.meego 1.0
//import Qt.labs.folderlistmodel 1.0

Page {
    id:selectorPage
    anchors.fill:parent
    tools: backTool

    Rectangle {
        id:pathbox
        anchors.top: parent.top
        width:parent.width
        height:48
        color:'white'
        Text{
            id:titlelabel
            anchors.fill: parent
            anchors.leftMargin: 5
            anchors.rightMargin: 50
            font { bold: true; family: "Helvetica"; pixelSize: 18 }
            color:"#cc6633"
            text:'Open File'
            verticalAlignment: "AlignVCenter"
        }
        Image{
            id:closeButton
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 4
            opacity: closeButtonArea.pressed ? 0.5 : 1.0
            //source:"image://theme/icon-m-dialog-common-close"
            source:"image://theme/icon-m-toolbar-close"
            MouseArea{
                id:closeButtonArea
                anchors.fill: parent
                onClicked: pageStack.pop()
            }
        }

    }

//    FolderListModel {
//         id: folderModel
//         showDotAndDotDot: true
//         showDirs: true
//     }

    ListView {
        id: view
        anchors.top: pathbox.bottom
        anchors.bottom: parent.bottom
        height: selectorPage.height - pathbox.height
        width: parent.width
        model: VisualDataModel {
            model: dirModel
            delegate: Rectangle {
                width:parent.width
                height: 80
                anchors.leftMargin: 10
                color:"black"
                Image {
                    id: iconFile
                    anchors.verticalCenter: parent.verticalCenter
                    width: 64; height: 64
                    source: "image://theme/"+view.model.model.fileIconName(view.model.modelIndex(index))
                }

                Column {
                    spacing: 10
                    //anchors.left: iconFile.left
                    anchors.leftMargin:10
                    anchors.left: parent.left
                    anchors.right: moreIcon.left

                    anchors.verticalCenter: parent.verticalCenter
                    Label {text:'<b>'+fileName+'</b>'
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 24
                        color:"white"
                        anchors.left: parent.left
                        anchors.right: parent.right

                    }
                    Label {text:filePath
                        font.family: "Nokia Pure Text"
                        font.pixelSize: 16
                        color: "#cc6633"
                        anchors.left: parent.left
                        anchors.right: parent.right
                    }
                }
                Image {
                    id:moreIcon
                    source: "image://theme/icon-m-common-drilldown-arrow-inverse"
                    anchors.right: parent.right;
                    anchors.verticalCenter: parent.verticalCenter
                    opacity:  ? 1 : 0
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        console.log(view.model.model)
                        if (view.model.model.isDir(view.model.modelIndex(index))){
                            titlelabel.text = 'Open File : ' + filePath
                            //previousFolderTool.currentFilePath = filePath
                            view.model.rootIndex = view.model.modelIndex(indeview.model.model.isDir(view.model.modelIndex(index))x)
                        }
                        else {
                            view.model.model.setCurrentPath(filePath)
                            rootWin.openFile(filePath)
                        }
                    }

                }
            }
        Component.onCompleted:{    
            view.model.rootIndex = view.model.model.getCurrentIndex()
            }
        }
    }


    ToolBarLayout {
        id:backTool
        visible: true
        ToolIcon {
            platformIconId: 'toolbar-back'
            onClicked: {
                view.model.rootIndex = view.model.parentModelIndex()
                titlelabel.text = 'Open File : ' + view.model.model.filePath(view.model.rootIndex)
            }
        }
    }
}

