/*!
 * 
 * Super simple wysiwyg editor v0.8.12
 * https://summernote.org
 * 
 * 
 * Copyright 2013- Alan Hong. and other contributors
 * summernote may be freely distributed under the MIT license.
 * 
 * Date: 2019-07-30T07:32Z
 * 
 */
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory();
	else if(typeof define === 'function' && define.amd)
		define([], factory);
	else {
		var a = factory();
		for(var i in a) (typeof exports === 'object' ? exports : root)[i] = a[i];
	}
})(window, function() {
return /******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 25);
/******/ })
/************************************************************************/
/******/ ({

/***/ 25:
/***/ (function(module, exports) {

(function ($) {
  $.extend($.summernote.lang, {
    'ja-JP': {
      font: {
        bold: '太字',
        italic: '斜体',
        underline: '下線',
        clear: 'クリア',
        height: '文字高',
        name: 'フォント',
        strikethrough: '取り消し線',
        subscript: 'Subscript',
        superscript: 'Superscript',
        size: '大きさ'
      },
      image: {
        image: '画像',
        insert: '画像挿入',
        resizeFull: '最大化',
        resizeHalf: '1/2',
        resizeQuarter: '1/4',
        floatLeft: '左寄せ',
        floatRight: '右寄せ',
        floatNone: '寄せ解除',
        shapeRounded: 'Shape: Rounded',
        shapeCircle: 'Shape: Circle',
        shapeThumbnail: 'Shape: Thumbnail',
        shapeNone: 'Shape: None',
        dragImageHere: 'ここに画像をドラッグしてください',
        dropImage: 'Drop image or Text',
        selectFromFiles: '画像ファイルを選ぶ',
        maximumFileSize: 'Maximum file size',
        maximumFileSizeError: 'Maximum file size exceeded.',
        url: 'URLから画像を挿入する',
        remove: '画像を削除する',
        original: 'Original'
      },
      video: {
        video: '動画',
        videoLink: '動画リンク',
        insert: '動画挿入',
        url: '動画のURL',
        providers: '(YouTube, Vimeo, Vine, Instagram, DailyMotion, Youku)'
      },
      link: {
        link: 'リンク',
        insert: 'リンク挿入',
        unlink: 'リンク解除',
        edit: '編集',
        textToDisplay: 'リンク文字列',
        url: 'URLを入力してください',
        openInNewWindow: '新しいウィンドウで開く'
      },
      table: {
        table: 'テーブル',
        addRowAbove: '行を上に追加',
        addRowBelow: '行を下に追加',
        addColLeft: '列を左に追加',
        addColRight: '列を右に追加',
        delRow: '行を削除',
        delCol: '列を削除',
        delTable: 'テーブルを削除'
      },
      hr: {
        insert: '水平線の挿入'
      },
      style: {
        style: 'スタイル',
        p: '標準',
        blockquote: '引用',
        pre: 'コード',
        h1: '見出し1',
        h2: '見出し2',
        h3: '見出し3',
        h4: '見出し4',
        h5: '見出し5',
        h6: '見出し6'
      },
      lists: {
        unordered: '通常リスト',
        ordered: '番号リスト'
      },
      options: {
        help: 'ヘルプ',
        fullscreen: 'フルスクリーン',
        codeview: 'コード表示'
      },
      paragraph: {
        paragraph: '文章',
        outdent: '字上げ',
        indent: '字下げ',
        left: '左寄せ',
        center: '中央寄せ',
        right: '右寄せ',
        justify: '均等割付'
      },
      color: {
        recent: '現在の色',
        more: 'もっと見る',
        background: '背景色',
        foreground: '文字色',
        transparent: '透明',
        setTransparent: '透明にする',
        reset: '標準',
        resetToDefault: '標準に戻す'
      },
      shortcut: {
        shortcuts: 'ショートカット',
        close: '閉じる',
        textFormatting: '文字フォーマット',
        action: 'アクション',
        paragraphFormatting: '文章フォーマット',
        documentStyle: 'ドキュメント形式',
        extraKeys: 'Extra keys'
      },
      help: {
        'insertParagraph': '改行挿入',
        'undo': '一旦、行った操作を戻す',
        'redo': '最後のコマンドをやり直す',
        'tab': 'Tab',
        'untab': 'タブ戻し',
        'bold': '太文字',
        'italic': '斜体',
        'underline': '下線',
        'strikethrough': '取り消し線',
        'removeFormat': '装飾を戻す',
        'justifyLeft': '左寄せ',
        'justifyCenter': '真ん中寄せ',
        'justifyRight': '右寄せ',
        'justifyFull': 'すべてを整列',
        'insertUnorderedList': '行頭に●を挿入',
        'insertOrderedList': '行頭に番号を挿入',
        'outdent': '字下げを戻す（アウトデント）',
        'indent': '字下げする（インデント）',
        'formatPara': '段落(P tag)指定',
        'formatH1': 'H1指定',
        'formatH2': 'H2指定',
        'formatH3': 'H3指定',
        'formatH4': 'H4指定',
        'formatH5': 'H5指定',
        'formatH6': 'H6指定',
        'insertHorizontalRule': '&lt;hr /&gt;を挿入',
        'linkDialog.show': 'リンク挿入'
      },
      history: {
        undo: '元に戻す',
        redo: 'やり直す'
      },
      specialChar: {
        specialChar: 'SPECIAL CHARACTERS',
        select: 'Select Special characters'
      }
    }
  });
})(jQuery);

/***/ })

/******/ });
});