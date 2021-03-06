{
  description = "gist manager";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix-src.url = "github:nix-community/poetry2nix";
    flake-compat = {
      url = "github:edolstra/flake-compat";
      flake = false;
    };
  };

  outputs = { self, nixpkgs, poetry2nix-src, flake-utils, flake-compat }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [
            poetry2nix-src.overlay
          ];
        };
        giz = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
        };
      in
        {
          # packages.x86_64-linux.hello = nixpkgs.legacyPackages.x86_64-linux.hello;

          # defaultPackage.x86_64-linux = self.packages.x86_64-linux.hello;
          defaultPackage = giz;
          defaultApp = flake-utils.lib.mkApp { drv = giz; };

          devShell = pkgs.mkShell {
            inputsFrom = [
              giz
            ];

            buildInputs = [
              pkgs.poetry
            ];
          };
        }
    );
}
