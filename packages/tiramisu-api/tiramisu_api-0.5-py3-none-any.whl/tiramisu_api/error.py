try:
    from tiramisu.error import APIError, ValueWarning, ValueOptionError, ValueErrorWarning, PropertiesOptionError, ConfigError, display_list
except ImportError:
    import weakref
    from .i18n import _

    def display_list(lst, separator='and', add_quote=False):
        if separator == 'and':
            separator = _('and')
        elif separator == 'or':
            separator = _('or')
        if isinstance(lst, tuple) or isinstance(lst, frozenset):
            lst = list(lst)
        if len(lst) == 1:
            ret = lst[0]
            if not isinstance(ret, str):
                ret = str(ret)
            if add_quote:
                ret = '"{}"'.format(ret)
            return ret
        else:
            lst.sort()
            lst_ = []
            for l in lst[:-1]:
                if not isinstance(l, str):
                    l = str(l)
                if add_quote:
                    l = '"{}"'.format(l)
                lst_.append(_(l))
            last = lst[-1]
            if not isinstance(last, str):
                last = str(_(last))
            if add_quote:
                last = '"{}"'.format(last)
            return ', '.join(lst_) + _(' {} ').format(separator) + '{}'.format(last)

    #____________________________________________________________
    # Exceptions for a Config
    class ConfigError(Exception):
        """attempt to change an option's owner without a value
        or in case of `_cfgimpl_descr` is None
        or if a calculation cannot be carried out"""
        def __init__(self,
                     exp,
                     ori_err=None):
            super().__init__(exp)
            self.ori_err = ori_err

    class APIError(Exception):
        pass

    class _CommonError:
        def __init__(self,
                     val,
                     display_type,
                     opt,
                     err_msg,
                     index):
            self.val = val
            self.display_type = display_type
            self.opt = weakref.ref(opt)
            self.err_msg = err_msg
            self.index = index
            super().__init__(self.err_msg)

        def __str__(self):
            try:
                msg = self.prefix
            except AttributeError:
                if self.opt() is None:
                    self.prefix = ''
                else:
                    self.prefix = self.tmpl.format(self.val,
                                                   self.display_type,
                                                   self.opt().impl_get_display_name())
                msg = self.prefix
            if self.err_msg:
                if msg:
                    msg += ', {}'.format(self.err_msg)
                else:
                    msg = self.err_msg
            if not msg:
                msg = _('invalid value')
            return msg

    class ValueWarning(_CommonError, UserWarning):
        tmpl = _('attention, "{0}" could be an invalid {1} for "{2}"')

    class ValueOptionError(_CommonError, ValueError):
        tmpl = _('"{0}" is an invalid {1} for "{2}"')

    class ValueErrorWarning(ValueWarning):
        tmpl = _('"{0}" is an invalid {1} for "{2}"')

    # Exceptions for an Option
    class PropertiesOptionError(AttributeError):
        "attempt to access to an option with a property that is not allowed"
        def __init__(self,
                     option_bag,
                     proptype,
                     settings,
                     opt_type=None,
                     requires=None,
                     name=None,
                     orig_opt=None):
            if opt_type:
                self._opt_type = opt_type
                self._requires = requires
                self._name = name
                self._orig_opt = orig_opt
            else:
                if option_bag.option.impl_is_optiondescription():
                    self._opt_type = 'optiondescription'
                else:
                    self._opt_type = 'option'
                self._requires = option_bag.option.impl_getrequires()
                self._name = option_bag.option.impl_get_display_name()
                self._orig_opt = None
            self._option_bag = option_bag
            self.proptype = proptype
            self._settings = settings
            self.msg = None
            super(PropertiesOptionError, self).__init__(None)

        def set_orig_opt(self, opt):
            self._orig_opt = opt

        def __str__(self):
            # this part is a bit slow, so only execute when display
            if self.msg:
                return self.msg
            if self._option_bag is None:
                return "option désactivée"
            req = self._settings.apply_requires(self._option_bag,
                                                True)
            # if req != {} or self._orig_opt is not None:
            if req != {}:
                only_one = len(req) == 1
                msg = []
                for action, msg_ in req.items():
                    msg.append('"{0}" ({1})'.format(action, display_list(msg_)))
                msg = display_list(msg)
            else:
                only_one = len(self.proptype) == 1
                msg = display_list(list(self.proptype), add_quote=True)
            if only_one:
                prop_msg = _('property')
            else:
                prop_msg = _('properties')
            if self._orig_opt:
                self.msg = str(_('cannot access to {0} "{1}" because "{2}" has {3} {4}'
                                 '').format(self._opt_type,
                                            self._orig_opt.impl_get_display_name(),
                                            self._name,
                                            prop_msg,
                                            msg))
            else:
                self.msg = str(_('cannot access to {0} "{1}" because has {2} {3}'
                                 '').format(self._opt_type,
                                            self._name,
                                            prop_msg,
                                            msg))
            del self._requires, self._opt_type, self._name, self._option_bag
            del self._settings, self._orig_opt
            return self.msg
