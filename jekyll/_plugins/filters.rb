module Jekyll
    module Filters
        def normalize_url(url)
            url.sub(/index\.html$/, "")
        end
    end
end
