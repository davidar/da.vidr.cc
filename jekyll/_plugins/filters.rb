module Jekyll
    module Filters
        def normalize_url(url)
            url.sub(/index\.html$/, "")
        end

        def summarize_post(content)
            content.sub(/<h.*/m, "<p><em>Continued after the jump...</em></p>")
        end
    end
end
