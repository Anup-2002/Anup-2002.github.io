# TODO

- [ ] Fix API schemas:
  - [ ] Add Pydantic `CoinRequest` and update `/generate-message` to accept body cleanly
  - [ ] Add Pydantic `PostRequest` and update `/post-chat` to accept JSON body
- [ ] Fix `/check-login` to use more reliable logic (reuse `post_chat` verification or check for editor/post availability differently)
- [ ] Improve `/post-chat` success verification (textbox cleared / post button disappears / toast)
- [ ] Optimize browser usage in full-flow (single browser/context, reuse across coins/pages)
- [ ] Save full-flow output to `output/results.json`
- [ ] Add logging to `logs/app.log` (coin URL, generated message, success/failure, exceptions)
- [ ] Add `schemas/` directory with:
  - [ ] `schemas/coin.py`
  - [ ] `schemas/message.py`
  - [ ] `schemas/post.py`
- [ ] Update README to reflect new request bodies and behavior
