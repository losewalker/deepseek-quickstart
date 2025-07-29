function main({data1}) {
    /**
     * 功能与Python markdown2.markdown()相同的Markdown解析器
     * @param {string} markdown - Markdown文本
     * @returns {string} HTML文本
     */
    function markdownToHtml(markdown) {
        // 预处理：标准化换行符
        let text = markdown.replace(/\r\n?/g, '\n');
        
        // 定义转换规则
        const rules = [
            // 标题 (1-6级)
            { regex: /^(#{1,6})\s*(.*?)\s*(?:#*\s*)?$/gm, replace: (m, hashes, content) => 
                `<h${hashes.length}>${content}</h${hashes.length}>` },
            
            // 水平线
            { regex: /^([*\-_] ?){3,}$/gm, replace: '<hr/>' },
            
            // 代码块
            { regex: /```([\s\S]*?)```/g, replace: '<pre><code>$1</code></pre>' },
            { regex: /~~~([\s\S]*?)~~~/g, replace: '<pre><code>$1</code></pre>' },
            { regex: / {4}(.*)/g, replace: '<pre><code>$1</code></pre>' },
            
            // 内联代码
            { regex: /`([^`]+)`/g, replace: '<code>$1</code>' },
            
            // 强调
            { regex: /\*\*(.*?)\*\*/g, replace: '<strong>$1</strong>' },
            { regex: /__(.*?)__/g, replace: '<strong>$1</strong>' },
            { regex: /\*(.*?)\*/g, replace: '<em>$1</em>' },
            { regex: /_(.*?)_/g, replace: '<em>$1</em>' },
            { regex: /~~(.*?)~~/g, replace: '<del>$1</del>' },
            
            // 链接和图片
            { regex: /!\[(.*?)\]\((.*?)\)/g, replace: '<img src="$2" alt="$1"/>' },
            { regex: /\[(.*?)\]\((.*?)\)/g, replace: '<a href="$2">$1</a>' },
            
            // 列表（无序和有序）
            { regex: /^\s*([*\-+])\s(.*)$/gm, replace: '<li>$2</li>' },
            { regex: /^\s*(\d+\.)\s(.*)$/gm, replace: '<li>$2</li>' },
            
            // 引用
            { regex: /^>\s*(.*)$/gm, replace: '<blockquote>$1</blockquote>' },
            
            // 段落（处理剩余文本）
            { regex: /^([^<\n].*)(?=\n{2}|$)/gm, replace: '<p>$1</p>' },
            
            // 换行
            { regex: /\n(?!\n)/g, replace: '<br/>' }
        ];
        
        // 特殊处理列表（包裹在ul/ol中）
        text = text.replace(/(<li>.*<\/li>(?:\n|$))+/g, (m) => {
            if (/^\s*\d/.test(m)) {
                return `<ol>${m}</ol>`;
            }
            return `<ul>${m}</ul>`;
        });
        
        // 应用所有转换规则
        rules.forEach(({regex, replace}) => {
            text = text.replace(regex, replace);
        });
        
        return text;
    }
    
    return {
        html: markdownToHtml(data1),
        markdown_content: data1
    };
}
