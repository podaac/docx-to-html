import React, { Component } from 'react'
import { saveAs } from 'file-saver'
import '../App.css';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'

class MainContent extends Component {
    constructor() {
        super()

        this.state = {
            html: '',
            filename: '',
            doNLP: false,
            makeTableOfContents: false,
            convertFTPLinks: false,
            submitError: false,
            fileSelectedError: false,
            wrongFileTypeError: false,
            tocModal: false,
            ftpModal: false,
            nlpModal: false,
            isLoading: false,
            fileUploadErrorList: [],
            count: 0,
            cssType: 'bootstrap',
        }
    }

    handleDoNLP = () => {
        this.state.doNLP ? this.setState({ doNLP: false }) : this.setState({ doNLP: true })
    }

    handleTableOfContents = () => {
        this.state.makeTableOfContents ? this.setState({ makeTableOfContents: false }) : this.setState({ makeTableOfContents: true })
    }

    handleFTPLinks = () => {
        this.state.convertFTPLinks ? this.setState({ convertFTPLinks: false }) : this.setState({ convertFTPLinks: true })
    }

    // sets css type the user chooses from the radio buttons
    handleCSSType = (type) => {
        this.setState({ cssType: type.target.value})
    }

    // handle modal show and close
    handleShowModal = (modalName) => {
        this.setState({ [modalName]: true })
    }

    closeModal = (modalName) => {
        this.setState({ [modalName]: false })
    }

    // handles loading spinner
    LoadingSpinner = () => {
        return this.state.isLoading ? <Spinner className="ml-2" animation="border" variant="success" /> : ''
    }

    // saves html file to users computer
    saveWithoutEdits = () => {
        const blob = new Blob([this.state.html], { type: "text/plain;charset=utf-8" })
        saveAs(blob, this.state.filename)
    }

    // adds filename of file that wasn't converted/errored to error message
    addErrorFileName = (filename) => {
        let filenamelist = this.state.fileUploadErrorList
        filenamelist.push(filename)
        this.setState({ fileUploadErrorList: filenamelist})
    }

    // decrement count for isLoading in .finally()
    decCount = () => {
        let c = this.state.count
        c--
        return this.setState({ count: c })
    }

    // docx form submit - POST request to server
    handleSubmit = (event) => {
        event.preventDefault()
        this.setState({ isLoading: true })
        this.setState({ wrongFileTypeError: false })
        this.setState({ submitError: false})
        this.setState({ fileUploadErrorList: []})

        // handle user not selecting a file
        if (this.uploadInput.files[0]) {
            this.setState({ fileSelectedError: false })
        } else {
            this.setState({ isLoading: false })
            this.setState({ fileSelectedError: true })
            return
        }

        // handle multiple file uploads at once
        let fileslist = this.uploadInput.files
        this.setState({ count: fileslist.length })

        // check file type - show error and skip file if not a docx
        for (let i = 0; i < fileslist.length; i++) {
            if (this.uploadInput.files[i].name.split('.').pop() !== 'docx') {
                this.setState({ wrongFileTypeError: true })
                this.setState({ isLoading: false })
                return
            }
        }

        // loop through each file and POST to server
        for (let i = 0; i < fileslist.length; i++) {
            // prepare data
            const data = new FormData();
            let uploadFileName = this.uploadInput.files[i].name
            let newFileName = uploadFileName.split('.').slice(0, -1).join('.')
            newFileName = newFileName + '.html'
            data.append('file', this.uploadInput.files[i])
            data.append('onlybootstrap', false)
            this.state.doNLP ? data.append('donlp', true) : data.append('donlp', false)
            this.state.makeTableOfContents ? data.append('toc', true) : data.append('toc', false)
            this.state.convertFTPLinks ? data.append('ftp', true) : data.append('ftp', false)
            data.append('csstype', this.state.cssType)

            // make api call - POST req - to the server 
            fetch('http://podaac-devwhale1.jpl.nasa.gov:8082/', {
            //fetch('http://localhost:8082/', {  
                method: 'POST',
                body: data,
            }).then((response) => {
                return response.json()
            }).then((data) => {
                this.setState({ submitError: false })
                this.setState({ html: data })
                
                // handle any converter errors
                if (this.state.html === 'error') {
                    this.decCount() 
                    this.addErrorFileName(this.uploadInput.files[i].name)
                    this.setState({ submitError: true })
                    return
                }

                this.setState({ filename: newFileName })
                this.decCount() 
                this.saveWithoutEdits() 
            }).catch((err) => {
                this.decCount() 
                this.addErrorFileName(this.uploadInput.files[i].name)
                this.setState({ submitError: true })
                return
            }).finally(() => {
                if (this.state.count === 0) {
                    this.setState({isLoading: false})
                }
            })
        } 
    }

    render() {
        return (
            <div className="container">
                <main className="text-center mt-5 mb-5"></main>
                <div className="row">
                    <div className="col text-center">
                        <form onSubmit={this.handleSubmit}>
                            <div>
                                <p className="errorStyle">{this.state.submitError ? 'Oops! Something went wrong' : ''}</p>
                                <p className="errorStyle">{this.state.fileUploadErrorList.length > 1 ? this.state.fileUploadErrorList.length + ' files were not converted' : ''}</p>
                                <p className="errorStyle">{this.state.fileUploadErrorList.length === 1 ? this.state.fileUploadErrorList.length + ' file was not converted' : ''}</p>
                                <p className="errorStyle">{this.state.fileSelectedError ? 'Oops! Please select a file' : ''}</p>
                                <p className="errorStyle">{this.state.wrongFileTypeError ? 'Oops! Wrong file type. Only DOCX files are permitted' : ''}</p>
                            </div>
                            <div className="form-group files">
                                <input className="my-1" ref={(ref) => { this.uploadInput = ref; }} type="file" accept=".docx" multiple/>
                                <this.LoadingSpinner />
                            </div>

                            <div className="form-check my-3">
                                <div className="row">
                                    <div className="col">
                                        <input type="checkbox" className="form-check-input" onClick={this.handleTableOfContents}/>
                                        <label className="form-check-label">Create Table of Contents</label>
                                        <sup><i className="fa fa-info-circle fa-lg ml-2 text-info" onClick={() => this.handleShowModal('tocModal')} /></sup>
                                    </div>
                                    <Modal show={this.state.tocModal} onHide={() => this.closeModal('tocModal')}>
                                        <Modal.Header>
                                            <Modal.Title>Create Table of Contents</Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            Creates a new Table of Contents from all of the header sections.
                                            Dynamically creates hyperlinks to each header section so the user can jump to sections.
                                                <br></br><br></br>
                                            If the docx file does not have any Header 1 or Header 2 sections specified, no table of contents will be made.
                                            </Modal.Body>
                                        <Modal.Footer>
                                            <Button variant="secondary" onClick={() => this.closeModal('tocModal')}>
                                                Close
                                                </Button>
                                        </Modal.Footer>
                                    </Modal>
                                </div> 
                            </div> 

                            <div className="form-check my-3">
                                <div className="row">
                                    <div className="col">
                                        <input type="checkbox" className="form-check-input" onClick={this.handleFTPLinks}/>
                                        <label className="form-check-label">Convert FTP Links to Drive</label>
                                        <sup><i className="fa fa-info-circle fa-lg ml-2 text-info" onClick={() => this.handleShowModal('ftpModal')} /></sup>
                                    </div>
                                    <Modal show={this.state.ftpModal} onHide={() => this.closeModal('ftpModal')}>
                                        <Modal.Header>
                                            <Modal.Title>Convert FTP Links to Drive</Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            Converts all FTP links to the corresponding drive link.
                                            Updates both the href and the visible link on the web page.
                                            <br></br><br></br>
                                            Does not convert any other references to FTP in the document outside of hyperlinks.
                                            </Modal.Body>
                                        <Modal.Footer>
                                            <Button variant="secondary" onClick={() => this.closeModal('ftpModal')}>
                                                Close
                                                </Button>
                                        </Modal.Footer>
                                    </Modal>
                                </div>
                            </div>
                            {/*}
                            <div className="form-check my-3">
                                <div className="row">
                                    <div className="col">
                                        <input type="checkbox" className="form-check-input" onClick={this.handleDoNLP} />
                                        <label className="form-check-label">Natural Language Processing (beta)</label>
                                        <sup><i className="fa fa-info-circle fa-lg ml-2 text-info" onClick={() => this.handleShowModal('nlpModal')} /></sup>
                                    </div>
                                    <Modal show={this.state.nlpModal} onHide={() => this.closeModal('nlpModal')}>
                                        <Modal.Header>
                                            <Modal.Title>Natural Language Processing</Modal.Title>
                                        </Modal.Header>
                                        <Modal.Body>
                                            Runs various Natural Langage Processing algorithms to dynamically change content in the document.
                                            <br></br><br></br>
                                            Can change header section titles based on a list of keywords or phrases specified.
                                            </Modal.Body>
                                        <Modal.Footer>
                                            <Button variant="secondary" onClick={() => this.closeModal('nlpModal')}>
                                                Close
                                                </Button>
                                        </Modal.Footer>
                                    </Modal>
                                </div>
                            </div>
                            */}

                            <div className="form-check my-3">
                                <div className="row">
                                    <div className="col" onChange={event => this.handleCSSType(event)}>
                                        <input type="radio" value="bootstrap" name="cssStyle" defaultChecked/> Bootstrap CSS
                                        <input className="ml-3" type="radio" value="podaac" name="cssStyle"/> PODAAC CSS (beta)
                                        <sup><i className="fa fa-info-circle fa-lg ml-2 text-info" onClick={() => this.handleShowModal('cssModal')} /></sup>
                                    </div>
                                </div>
                                <Modal show={this.state.cssModal} onHide={() => this.closeModal('cssModal')}>
                                    <Modal.Header>
                                        <Modal.Title>CSS Styling</Modal.Title>
                                    </Modal.Header>
                                    <Modal.Body>
                                        Choose between Bootstrap 4 or PODAAC CSS styling. 
                                        <br></br><br></br>
                                        <b>Bootstrap</b><br></br>
                                        Adds header and footer. Adds bootstrap styling to img tags, table tags and adds a container tag. Adds link to Bootstrap CDN.
                                        <br></br><br></br>
                                        <b>PODAAC</b><br></br>
                                        Adds header and footer. Adds links to all PODAAC CSS stylesheets.
                                    </Modal.Body>
                                    <Modal.Footer>
                                        <Button variant="secondary" onClick={() => this.closeModal('cssModal')}>
                                            Close
                                        </Button>
                                    </Modal.Footer>
                                </Modal>
                            </div>
                            <button className="btn btn-primary">{this.state.isLoading ? 'Loading...' : 'Upload'}</button> 
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}

export default MainContent