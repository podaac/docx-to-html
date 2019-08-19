import React, { Component } from 'react'
import { Editor, EditorState, RichUtils, convertFromHTML, ContentState } from 'draft-js'
import { stateToHTML } from 'draft-js-export-html'


/****************************
 * not using any of this now
 *  *************************/ 

// this would be useful in the case that a PDF to HTML conversion works, since PDF can't be edited prior to conversion

class WYSIWYGEditor extends Component {
    constructor() {
        super()

        this.state = {
            editorState: EditorState.createEmpty(),
        }
        this.focus = () => this.refs.editor.focus();
        this.onChange = (editorState) => this.setState({ editorState });

        //this.handleKeyCommand = (command) => this._handleKeyCommand(command);
        this.onTab = (e) => this._onTab(e);
        this.toggleBlockType = (type) => this._toggleBlockType(type);
        this.toggleInlineStyle = (style) => this._toggleInlineStyle(style);
    }

    /****************
     * editor stuff *
     ****************/
    
    //save after wysiwyg edits have been made
    saveWYSIWYG = (editorState) => {
        const contentState = this.state.editorState.getCurrentContent()
        let output = stateToHTML(contentState)

        const data = new FormData()
        data.append('onlybootstrap', true)
        data.append('htmloutput', output)
        data.append('donlp', false)
        data.append('toc', false)

        fetch('http://localhost:80/', {
            method: 'POST',
            body: data,
        }).then((response) => {
            return response.json()
        }).then((data) => {
            this.setState({ html: data })
            return this.saveWithoutEdits()
        }).catch((err) => {
            console.log(err)
        })
    }

    //loads html into editor
    loadHTML = () => {
        const blocksFromHTML = convertFromHTML(this.state.html)
        const state = ContentState.createFromBlockArray(
            blocksFromHTML.contentBlocks,
            blocksFromHTML.entityMap
        )
        this.setState({ editorState: EditorState.createWithContent(state) })
    }

    handleKeyCommand = (command) => {
        const newState = RichUtils.handleKeyCommand(this.state.editorState, command)
        if (newState) {
            this.onChange(newState);
            return 'handled';
        }
        return 'not-handled';
    }

    _onTab(e) {
        const maxDepth = 4;
        this.onChange(RichUtils.onTab(e, this.state.editorState, maxDepth));
    }
    _toggleBlockType(blockType) {
        this.onChange(
            RichUtils.toggleBlockType(
                this.state.editorState,
                blockType
            )
        );
    }

    _toggleInlineStyle(inlineStyle) {
        this.onChange(
            RichUtils.toggleInlineStyle(
                this.state.editorState,
                inlineStyle
            )
        );
    } 

    render() {
        return (
            <div className="container">
                <main className="text-left mt-5 mb-5">
                            {/*
                            <div className="form-check my-3">
                                <input type="checkbox" className="form-check-input" onClick={this.handleMakeCustomEdits}/>
                                <label className="form-check-label">Make Custom Edits (beta)</label>
                            </div> 
                            */}
                </main>

                <div className="RichEditor-root my-4">
                    <BlockStyleControls
                        editorState={this.state.editorState}
                        onToggle={this.toggleBlockType}
                    />
                    <InlineStyleControls
                        editorState={this.state.editorState}
                        onToggle={this.toggleInlineStyle}
                    />
                    <div className="border "></div>
                    <div className={this.state.className} onClick={this.focus}>
                        <Editor
                            blockStyleFn={getBlockStyle}
                            customStyleMap={styleMap}
                            editorState={this.state.editorState}
                            handleKeyCommand={this.handleKeyCommand}
                            onChange={this.onChange}
                            onTab={this.onTab}
                            placeholder="Upload a DOCX file to edit..."
                            ref="editor"
                            spellCheck={true}
                        />
                    </div>
                </div>
                <button onClick={this.saveWYSIWYG} className="btn btn-primary">Save</button>
            </div>
        )
    }
}

 /****************
 * editor stuff *
 * ***************/


// Custom overrides for "code" style.
const styleMap = {
    CODE: {
        backgroundColor: 'rgba(0, 0, 0, 0.05)',
        fontFamily: '"Inconsolata", "Menlo", "Consolas", monospace',
        fontSize: 16,
        padding: 2,
    },
};

function getBlockStyle(block) {
    switch (block.getType()) {
        case 'blockquote': return 'RichEditor-blockquote';
        default: return null;
    }
}

class StyleButton extends React.Component {
    constructor() {
        super();
        this.onToggle = (e) => {
            e.preventDefault();
            this.props.onToggle(this.props.style);
        };
    }

    render() {
        let className = 'RichEditor-styleButton';
        if (this.props.active) {
            className += ' RichEditor-activeButton';
        }

        return (
            <span className={className} onMouseDown={this.onToggle}>
                {this.props.label}
            </span>
        );
    }
}


const BLOCK_TYPES = [
    { label: 'H1', style: 'header-one' },
    { label: 'H2', style: 'header-two' },
    { label: 'H3', style: 'header-three' },
    { label: 'H4', style: 'header-four' },
    { label: 'H5', style: 'header-five' },
    { label: 'H6', style: 'header-six' },
    { label: 'Blockquote', style: 'blockquote' },
    { label: 'UL', style: 'unordered-list-item' },
    { label: 'OL', style: 'ordered-list-item' },
    { label: 'Code Block', style: 'code-block' },
];

const BlockStyleControls = (props) => {
    const { editorState } = props;
    const selection = editorState.getSelection();
    const blockType = editorState
        .getCurrentContent()
        .getBlockForKey(selection.getStartKey())
        .getType();

    return (
        <div className="RichEditor-controls">
            {BLOCK_TYPES.map((type) =>
                <StyleButton
                    key={type.label}
                    active={type.style === blockType}
                    label={type.label}
                    onToggle={props.onToggle}
                    style={type.style}
                />
            )}
        </div>
    );
};

var INLINE_STYLES = [
    { label: 'Bold', style: 'BOLD' },
    { label: 'Italic', style: 'ITALIC' },
    { label: 'Underline', style: 'UNDERLINE' },
    { label: 'Monospace', style: 'CODE' },
];

const InlineStyleControls = (props) => {
    var currentStyle = props.editorState.getCurrentInlineStyle();
    return (
        <div className="RichEditor-controls">
            {INLINE_STYLES.map(type =>
                <StyleButton
                    key={type.label}
                    active={currentStyle.has(type.style)}
                    label={type.label}
                    onToggle={props.onToggle}
                    style={type.style}
                />
            )}
        </div>
    );
};


export default WYSIWYGEditor