{ pkgs, ... }:

{
  languages.python.enable = true;
  languages.python.package = pkgs.python312;
  languages.python.venv.enable = true;


  # https://devenv.sh/languages/
  # languages.nix.enable = true;

  # https://devenv.sh/pre-commit-hooks/
  # pre-commit.hooks.shellcheck.enable = true;

  # https://devenv.sh/processes/
  # processes.ping.exec = "ping example.com";

  # See full reference at https://devenv.sh/reference/options/
}
