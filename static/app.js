const container = document.getElementById("container")
const coinLimits = document.getElementById("coin-limits")
const limited = document.getElementById("limited")
const coinPosts = document.getElementById("coin-posts")

fetch("static/data.json").then(res => res.json()).then(data => {
    
    if (data.hasOwnProperty("error")) {
        const html = `
            <h2 class=error>${data.error}</h2>
        `       
        container.innerHTML = html
    } else {
        let { coins, limits, posts } = data

        let coinsHtml = ""
        
        for (let coin in posts) {
            const limit = posts[coin].length
            let overLimit = ""
            if (coins.includes(coin)) {
                overLimit = "over-limit"
            }
            coinsHtml += `
                            <div class="limit">
                                <p>${coin}</p>
                                <p class=${overLimit}>${limit}</p>
                            </div>
                        `
        }


        coins = coins.map(coin => `
            <div class="coin">
                <p>${coin}</p>
            </div>
        `)
        limits = limits.map(coin => `
            <div class="limit">
                <p>${coin.symbol}</p>
                <p>${coin.limit}</p>
            </div>
        `)
        limited.innerHTML = coins.join("")
        coinLimits.innerHTML += limits.join("")
        coinPosts.innerHTML = coinsHtml
    }
})