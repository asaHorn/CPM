import discord
from discord.ext import commands
from time import localtime, strftime


class pwdStore:
    pwds = dict()
    topo = dict()

    def __init__(self):
        pass

    def addTopo(self, topoStr: str):
        topoList = topoStr.split(' ')
        for line in topoList:
            if line == '':
                continue
            lineList = line.split(':')
            self.topo[lineList[0]] = lineList[1].lower()

        # error handling here
        return 'added topo: ``` ' + str(self.topo) + '```'

    def exists(self, user: str, box: str):
        try:
            self.prettyGetPwd(user, box)
        except KeyError:
            return False
        return True

    def addPwd(self, user: str, box: str, pwd: str, tags=None):
        if tags is None:
            tags = []

        ret = '```'
        carrots = 0
        for x in tags:
            if x[0] == '^':
                carrots += 1

        OS = ''
        if carrots > 1:
            ret += '**Critical: multiple tags given for box type.**  \n'
            ret = 'Unable to add password...' + ret
        elif carrots == 0:
            try:
                OS = self.topo[box]
            except KeyError:
                ret += box + ' is not a known machine it will be tagged as ^uncategorized. To fix this add ' + box + \
                       ' to the topo using $addTopo ' + box + ':(desired tag) then rerun this command. Or rerun this ' \
                                                              'command with a OS tag $new <user> <box> ^(OS here)\n'
                self.topo[box] = 'uncategorized'
                OS = self.topo[box]
        else:
            try:
                OS = self.topo[box]
                ret += box + ' is already registered in the topo as a' + OS + '. Using given OS tag. To use ' \
                       'preregistered OS tag rerun this command with the correct tag or without a tag. To update ' \
                       'the topo use $addTopo ' + box + ':<new tag>.\n'
                for x in tags:
                    if x[0] == '^':
                        OS = x[1:].lower()
                        tags.remove(x)
                        break
            except KeyError:
                for x in tags:
                    if x[0] == '^':
                        OS = x[1:].lower()
                        self.topo[box] = x[1:].lower()
                        tags.remove(x)
                        break

        ret += '```'

        self.pwds[self.makeID(user, box)] = pwd, OS, tags,
        return ret

    def getPwd(self, user: str, box: str):
        return self.pwds[self.makeID(user, box)][0]

    def prettyGetPwd(self, user: str, box: str):
        return self.makeID(user, box) + ': ' + self.getPwd(user, box)

    def makeID(self, user: str, box: str):
        return box + '/' + user

    def display(self):
        if len(self.pwds) == 0:
            embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                                  description="CPM isn't currently tracking anything", color=0xff0000)

        else:
            counter = 0
            groups = 0
            entryList = []
            for entry in self.pwds:  # this is lots of fun lists and dicts huh? makes list of lists of like OS boxes,
                counter += 1
                foundGroup = False  # list of Linux, list of Windows etc
                for group in entryList:
                    if self.pwds[entry][1] == self.pwds[group[0]][1]:  # if the entry we are checking's OS tag == the OS tag
                        group.append(entry)                            # of the first element of group (guaranteed to exist)
                        foundGroup = True
                        break
                if not foundGroup:  # if we didn't find correct spot we make our own!
                    entryList.append([entry,])

            print('Updating display. Tracking passwords for the following boxes:')
            for group in entryList:  # sort every group to keep display nice and orderly
                group.sort()

                lastBox = ''
                for x in group:
                    if x.split('/')[0] != lastBox:
                        groups += 1
                        lastBox = x.split('/')[0]
                        print(lastBox)

            print()
            embed = discord.Embed(title="source", url="https://github.com/asaHorn/CPM",
                                  description="CPM tracking " + str(counter) + " passwords over " + str(groups) +
                                              " systems",
                                  color=0xff0000)

            for group in entryList:
                counter = ""
                users = ""
                passwords = ""
                tags = ""

                for entry in group:
                    users += entry + '\n'
                    passwords += self.pwds[entry][0] + '\n'
                    tags += str(self.pwds[entry][2])[1:-1] + '\n'

                embed.add_field(name=self.pwds[group[0]][1], value=users, inline=True)
                embed.add_field(name="​", value=passwords, inline=True)
                embed.add_field(name="​", value=tags + '​', inline=True)

        embed.set_author(name="CPM")
        embed.set_footer(text="last updated: " + strftime("%I:%M:%S %p", localtime()))
        return embed
        # todo group entries by type (net, windows, linux) then location (cloud, LAN, other stuff) then by box.

        # todo colors

        # todo pretty headings
