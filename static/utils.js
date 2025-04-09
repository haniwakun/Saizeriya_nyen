// クエリパラメータをオブジェクトから生成してURLにセット
function buildUrl(path, params = {}) {
    const url = new URL(path, window.location.origin);
    for (const [key, value] of Object.entries(params)) {
        if (value !== undefined && value !== null && value !== "") {
            url.searchParams.set(key, value);
        }
    }
    return url.toString();
}

// 数字入力チェック
function isNumeric(value) {
    return /^\d+$/.test(value);
}