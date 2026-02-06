<!-- ---
!-- Timestamp: 2026-02-06 19:01:09
!-- Author: ywatanabe
!-- File: /home/ywatanabe/proj/scitex-linter/GITIGNORED/AS_PLUGIN.md
!-- --- -->

ruff を拡張、みたいな感じにできたりしないのかな

6:59 PM
いいアイデアだけど、ruffはRust製でプラグインシステムがまだない。カスタムルールを追加するにはruff本体をforkしてRustで書く必要があって、現実的じゃない。

現実的な選択肢としては：

flake8プラグインが一番筋がいい。flake8はPythonプラグインをpipで配布でき、pip install flake8-scitexで使えるようになる。ASTベースのチェッカーをそのまま流用できるし、既存のエディタ統合（VS Code, Emacs）が全部タダで付いてくる。stx-lintで書いたロジックをほぼそのままflake8のインターフェースに載せるだけ。

pylint pluginも可能だけど、flake8の方がエコシステムが広いし軽い。

ruff対応は、ruff側がプラグインAPIを公開するのを待つか、.ruff.tomlのextend-selectで将来的に対応されるのを期待するしかない。ただしruffのGitHubでplugin systemは長く議論されていて、いつ来るかは不明。

現実的なロードマップとしては、今のstx-lintをスタンドアロンで動かしつつ、flake8プラグインとしても配布する形が一番早くて互換性も高い。flake8プラグイン化は構造的には半日仕事で、setup.pyのentry pointに登録するだけ。やる？

<!-- EOF -->