window.TIEOUT_REPO = "ZP-Projects/wbs-link";
// Optional privacy-friendly analytics (e.g. GoatCounter): paste your site code, e.g. "wbslink". Leave "" to disable.
window.TIEOUT_GOATCOUNTER = "";
(function(){var c=window.TIEOUT_GOATCOUNTER;if(!c)return;var s=document.createElement("script");s.async=true;s.dataset.goatcounter="https://"+c+".goatcounter.com/count";s.src="https://gc.zgo.at/count.js";document.head.appendChild(s);})();
document.addEventListener("DOMContentLoaded",function(){var r=window.TIEOUT_REPO;document.querySelectorAll("[data-gh]").forEach(function(a){a.href="https://github.com/"+r+a.getAttribute("data-gh");});});
