# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command


# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()


# https://github.com/ranger/ranger/wiki/Integrating-File-Search-with-fzf
# Now, simply bind this function to a key, by adding this to your ~/.config/ranger/rc.conf: map <C-f> fzf_select
class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        if self.quantifier:
            # match only directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        else:
            # match files and directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
# fzf_locate
class fzf_locate(Command):
    """
    :fzf_locate

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        if self.quantifier:
            command="locate home | fzf -e -i"
        else:
            command="locate home | fzf -e -i"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)


class rclone_send_file(Command):
    def execute(self):
        if self.fm.thisfile:
            selected_file = self.fm.thisfile.path
            print(f'selected_file: {selected_file}')
            # /home/ph/Documents/sync_vault
            #  self.fm.run(f'rclone copy "{selected_file}" sync-vault:/sync_vault --progress --stats-one-line -v --create-empty-src-dirs --fast-list --transfers=8 --checkers=16')
        #  rclone copy /home/ph/Documents/sync_vault/Personal🧑/1.Definition/1.Routine.md sync-vault:/sync_vault/Personal🧑/1.Definition/ --progress --stats-one-line -v --create-empty-src-dirs --fast-list --transfers=8 --checkers=16
        else:
            self.fm.notify("No file selected!")

class rclone_get_file(Command):
    def execute(self):
        if self.fm.thisfile:
            selected_file = self.fm.thisfile.path
            self.fm.run(f'rclone copy sync-vault:/sync_vault/"{selected_file}" . --progress --stats-one-line -v --create-empty-src-dirs --fast-list --transfers=8 --checkers=16')
        else:
            self.fm.notify("No file selected!")

class llmr_with_files(Command):
    """
    Send selected files to llmr command
    """
    def execute(self):
        import subprocess

        # Get selected files or current file if none selected
        if self.fm.thistab.get_selection():
            selected_files = [f.path for f in self.fm.thistab.get_selection()]
        elif self.fm.thisfile:
            selected_files = [self.fm.thisfile.path]
        else:
            self.fm.notify("No files selected!")
            return

        # Build the command
        cmd = ['alacritty', '--option', 'font.size=20', '-e', 'bash', '-c']

        # Construct the llmr command with files
        llmr_cmd = f"llmr openai/gpt-4.1 default {' '.join(selected_files)}"
        shell_cmd = f'export PATH="$PATH:/home/{os.environ["USER"]}/.local/bin"; echo "{llmr_cmd}"; {llmr_cmd}; exec bash'

        cmd.append(shell_cmd)

        # Run the command
        subprocess.Popen(cmd)
