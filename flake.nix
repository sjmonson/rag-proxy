{
  description = "RAG Demo";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
      in
      {
        packages.default = mkPoetryApplication {
          projectDir = ./.;
          # Just let wheels handle deps
          preferWheels = true;
        };

        devShells.default = pkgs.mkShell {
          #inputsFrom = [ self.packages.${system}.default ];
          packages = with pkgs; [ poetry ];
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib/";
          # Execs the current shell
          #shellHook = ''exec zsh'';
        };
      });
}
