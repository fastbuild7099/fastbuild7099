const axios = require("axios");
const http = require("http");
const https = require("https");

const _http = axios.create({
  timeout: 15 * 1000,
  httpsAgent: new https.Agent({ keepAlive: true, rejectUnauthorized: false }),
  httpAgent: new http.Agent({ keepAlive: true }),
  baseURL: "https://drpy.yanshanxiyu.top:443/api/%E9%87%87%E9%9B%86%E4%B9%8B%E7%8E%8B[%E5%90%88]?extend=H4sIAAAAAAAAA9PT088qzs%2FTf9ne%2FnJ2W3RVZezLuTOfNTTqgURVDAGu%2FMCKHwAAAA%3D%3D&filter=true", //替换成其他地址
});

const fetch = async (req) => {
  delete req.query["token"];
  const { flag, play } = req.query;
  if (
    play &&
    /\.(m3u8|mp4|rmvb|avi|wmv|flv|mkv|webm|mov|m3u)(?!\w)/i.test(play)
  ) {
    return {
      url: play,
      jx: 0,
      parse: 0,
    };
  }

  const ret = await _http("", {
    params: req.query,
  });
  return ret.data;
};

const meta = {
  key: "cwzy", //key不能与其他site冲突
  name: "18+采王自用",
  type: 4,
  api: "/video/cwzy", //使用相对地址，服务会自动处理，不能与其他site冲突
  searchable: 1,
  quickSearch: 1,
  changeable: 0,
};

module.exports = async (app, opt) => {
  app.get(meta.api, fetch);
  opt.sites.push(meta);
};
