const container = document.getElementById("container");
const coinLimits = document.getElementById("coin-limits");
const limited = document.getElementById("limited");
const coinPosts = document.getElementById("coin-posts");

(async function () {
   const responses = await Promise.all([
      fetch("static/data.json"),
      fetch("static/images.json")
   ]);
   const data = await responses[0].json();
   const images = await responses[1].json();

   for (let key in data.posts) {
      data.posts[key].image = images[key.toLowerCase()];
   }

   for (let item of data.limits) {
      item.image = images[item.symbol.toLowerCase()];
   }

   displayLimits(data, images);
})();

function displayLimits(data, images) {
   if (data.hasOwnProperty("error")) {
      const html = `
         <h2 class=error>${data.error}</h2>
     `;
      container.innerHTML = html;
   } else {
      let { coins, limits, posts } = data;
      let coinsHtml = "";

      for (let coin in posts) {
         const maxLimit = findMaxLimit(coin, limits);

         const limit = posts[coin].length;

         const limitClass = getLimitClass(limit, maxLimit);

         coinsHtml += `
            <div class="box ${limitClass}" >
               <img class="icon" src=${posts[coin].image} />
               <div class="limit">
                  <p class=${
                     coin.length >= 7 ? "x-small" : coin.length >= 5 ? "small" : ""
                  }>${coin}</p>
               </div>
               <p class=${limitClass}>${limit}</p>
            </div>
         `;
      }
      coins =
         coins.length > 0
            ? coins.map(
                 (coin) => `
            <div class="box">
               <img class="icon" src=${images[coin.toLowerCase()]} />
               <div class="limit">
                  <p class=${
                     coin.length >= 7 ? "x-small" : coin.length >= 5 ? "small" : ""
                  }>${coin}</p>
               </div>
            </div>
         `
              )
            : [`<p>There is no coins currently at the limit.</p>`];
      limits = limits.map(
         (coin) => `
            <div class="box">
               <img class="icon" src=${coin.image} />
               <div class="limit">
                  <p>${coin.symbol}</p>
               </div>
               <p>${coin.limit}</p>
            </div>
         `
      );

      limited.innerHTML = coins.join("");
      coinLimits.innerHTML += limits.join("");
      coinPosts.innerHTML = coinsHtml;
   }
}

function findMaxLimit(coin, limits) {
   const maxposts = limits.find((limit) => limit.symbol === coin);
   return maxposts ? maxposts.limit : 2;
}

function getLimitClass(limit, maxLimit) {
   if (limit >= maxLimit) {
      return "overlimit";
   }

   if (maxLimit - limit === 1) {
      return "warning";
   }
   return "";
}
