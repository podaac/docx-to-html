import React, {Component} from 'react'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'



class FooterContent extends Component {
    constructor() {
        super()

        this.state = {
            quickGuide: false,
        }
    }

    //handle modal show and close
    handleShowModal = (modalName) => {
        this.setState({ [modalName]: true })
    }

    closeModal = (modalName) => {
        this.setState({ [modalName]: false })
    }

    render() {
        return (
            <footer className="footer container mt-5 border-top text-center">
                <div className="row">
                    <div className="col mt-3">
                        <Button className="m-2 btn btn-secondary" onClick={() => this.handleShowModal('quickGuide')}>Quick Guide</Button>
                        <Button className="m-2 btn btn-secondary" href="https://podaac-git.jpl.nasa.gov:8443/ajoseph/docx2html-docker-app" target="_blank">Gitlab</Button>
                    </div>
                </div>

                <Modal show={this.state.quickGuide} onHide={() => this.closeModal('quickGuide')}>
                    <Modal.Header>
                        <Modal.Title>Quick Guide</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        This is a quick tutorial & short reference. To read more about this app, look at source code, download the app and/or contribute, visit the <a href="https://podaac-git.jpl.nasa.gov:8443/ajoseph/docx2html-docker-app">Gitlab</a> page.
                        <br></br><br></br>
                        <b>DOCX to HTML file conversion</b><br></br>
                        The app converts any DOCX file to HTML. It uses the DOCX formatting to create equivalent HTML formatting (ie. Header 1 in DOCX => h1 in HTML). 
                        <br></br><br></br>
                        <b>Beautiful Soup 4 (BS4)</b><br></br>
                        A Python 3 HTML parser. BS4 allows us to parse the HTML document and dynamically modify, add, delete and have access to elements, text, HTML tags and more.
                        <br></br><br></br>
                        <b>Bootstrap CSS</b><br></br>
                        By parsing the HTML with BS4 we can add CSS styles, classes and id tags. We're able to add the Bootstrap CDN to the head tag and then add Bootstrap classes, tags and elements to style the HTML. This allows us to create a styled mobile friendly HTML page.
                        <br></br><br></br>
                        <b>This app supports PNG & JPG images</b>. It will also convert TIFF, EMF & WMF to PNG but this may cause problems. If your images are not displaying on the webpage, try converting them to PNG or JPG before uploading them.
                        <br></br><br></br>
                        <b>DOC files are not supported</b>. Convert any DOC file to DOCX before uploading.
                        <br></br><br></br>
                        <b>Table of Contents</b><br></br>
                        To create a dynamic Table of Contents, have all of the section headings labed as Header 2 prior to uploading. The DOCX file should have a single Header 1 and each section labeled as Header 2. Sub sections should be labeled as Header 3
                        <br></br><br></br>
                        <b>Convert FTP Links to Drive</b><br></br>
                        All FTP links get converted to their corresponding Drive links. Only the href and text inside the 'a tag' will be converted. Any references to FTP outside of this will be left alone.
                        <br></br><br></br>
                        <b>Natural Language Processing</b><br></br>
                        TO DO
                        <br></br><br></br>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={() => this.closeModal('quickGuide')}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Modal>
            </footer>
        )
    }
}

export default FooterContent